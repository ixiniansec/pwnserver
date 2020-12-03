## PwnServer

PwnServer is a vulnerability scanning tool that supports highly customized POC. The program functions include IP location query, CMS information query, port scanning, path scanning and vulnerability scanning.



#### Installation：

```bash
git clone https://github.com/ixiniansec/pwnserver.git
cd pwnserver
```

#### Usage：

Please read the wiki:https://github.com/ixiniansec/pwnserver/wiki

#### Import POC：

- Create a new directory and import POC (other POC not included in the current project)：

1. Create a folder under `pwnserver/scripts/poc` and add the file `POC_batch_process.py`；

2. Create `POC_standard` file；

   Note: `POC_standard` needs to be in the newly created folder.

   ```bash
   #!/usr/bin/bash
   SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
   
   python3 $SHELL_FOLDER/xxxx_poc.py <info>
   
   '''
   Here you can add POC according to the above format.
   Note: <info> represents the parameters required by POC.
   
   info reference:
   <port>
   <url>
   <cookice>
   <token>
   #About the solution that requires other parameters:
   #Modify POC_batch_process.py, add the required parameters.
   '''
   ```

- Import a new POC (the directory exists by default):

  Import POC, modify `POC_standard` to add new POC execution statement.

- `python3 $SHELL_FOLDER/xxxx_poc.py <info>`

  

  ###### NOTE:

  You can get `POC_standard` and `POC_batch_process.py` in the data directory

#### About unrecognized CMS&CMS query API call failure：

The program uses whatcms API. The free version only has 1000 queries a month. If you find that you cannot use it, please register whatcms and modify the CMS query key in scan.py.



#### Other problems：

Q: How to automatically call POC when there is a loophole?

A: This version is not currently supported.

Q: The port scan failed?

A: The principle of port scanning in this program is connect. If it cannot be used normally, please check whether the network is normal or whether the target firewall is blocking it.

solution:

Try using other scanners.

Q: If the port scan fails, the program will automatically exit and no more vulnerability scan?

A: Please comment the port scanning code segment, the new version will add the --vulscan function.

If you have other questions, please submit issues.

#### Precautions：

The program currently does not support verification of websites with CDNs.



#### Thanks：

https://github.com/zhzyker/exphub

https://github.com/Esonhugh

#### License：

MIT License
