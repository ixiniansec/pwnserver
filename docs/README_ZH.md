## PwnServer

PwnServer是一個支持高度自定義POC的漏洞掃描工具，程序功能包含IP位置查詢、CMS信息查詢、端口掃描、路徑掃描和漏洞掃描。



#### 安裝：

```bash
git clone https://github.com/ixiniansec/pwnserver.git
cd pwnserver
```

#### 使用：

請閱讀https://github.com/ixiniansec/pwnserver/wiki



#### 導入POC：

- 建立新目錄導入POC（目前項目未收錄的其他POC）：

1. 在`pwnserver/scripts/poc`下創建文件夾，加入`POC_batch_process.py`文件；

2. 創建`POC_standard`文件；

   注意：`POC_standard`需要在新創建文件夾下。
   
   ```bash
   #!/usr/bin/bash
   SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
   
   python3 $SHELL_FOLDER/xxxx_poc.py <info>
   '''
   在這裏按照上面的格式添加POC即可。
   注意：<info>表示POC需要的參數。
   
   info參考：
   <port> 
   <url>
   <cookice>
   <token>
   #關於需要其他參數的解決方案：
   #修改POC_batch_process.py，加入需要的參數。
   '''
   ```

- 導入新POC（默認存在該目錄）：

  導入POC，修改`POC_standard` 添加新POC執行語句。

  `python3 $SHELL_FOLDER/xxxx_poc.py <info>`
  
  
  
  ###### NOTE:
  
  您可以在data目錄獲得`POC_standard`和`POC_batch_process.py`

#### 關於無法識別CMS&CMS查詢API調用失敗：

該程序使用whatcms的API。免費版一個月只有1000次查詢，如果您發現不能使用，請註冊whatcms，修改scan.py中CMS查詢的key.



#### 其他問題：

Q：如何實現存在漏洞即自動調用POC？

A：該版本暫不支持。

Q：端口掃描失敗？

A：本程序端口掃描原理是connect，如果不能正常使用，請檢查網路是否正常或者目標防火牆是否攔截。

解決方案：

使用其他掃描器嘗試。

Q：端口掃描失敗程序自動退出，不再進行漏洞掃描？

A：請註釋端口掃描代碼段，新版本將加入--vulscan功能。

如果您還有其他問題，請提交issues.



#### 注意事項：

該程序目前不支持對存在CDN的網站驗證。



#### 鳴謝：

https://github.com/zhzyker/exphub

https://github.com/Esonhugh

#### 許可證：

MIT License

