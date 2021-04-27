# Protocol defining

## The protocol:

### Client: 
    Send its registering information through TCP, including its Name, IP addr, UDP port (to recieve server's info), current date/time 

### Server:
        - After receiving registering information from the client, server send the unit id of client, the tcp port and the interval to the client.
        - Server can send message to the client through the udp port client sent.
        - Reply to registering packets:
            "!SUCC + [info]"
            or "!FAIL + [error]"
        - When sending the change in interval time, if within 5s the server doesn't receive the received change message from the client then the server will resend the change.

### Clean disconnection:
    Sent the message "!DISC" to confirm clients' disconnection.        

#### Msg format: 
    [msg's length] + [5 bytes command abbriviation] + [data]
>Consider changing this, maybe the length is redundant.

#### Registering packet: 
    "!RGTR + [info]"
#### Succeeeded register confirmation packet:
    "!SUCC + [info]"
#### Failed register confirmation packet (connect tới được nhưng không đăng kí được):
    "!FAIL + [info]"
##### Scenario:
`client` kết nối tới `server` lần đầu thông qua địa chỉ `(ip_addr, port)`, có thể có các trường hợp sau xảy ra:
- `client` tạo đường connect thành công tới `server`:
    - `server` gửi Succeeded register confirmation packet về cho `client`.
    - Từ đây `server` listen trên 1 port đã chỉ định cho `client` gửi thông tin về. (quay lại check việc tạo đường connect lần đầu).
- `client` không tạo được đường connect tới `server`:
    - `server` lỗi: Error handling
    - `client` lỗi: Error handling, kiếm cách để connect lại.
    - Các lỗi thường gặp: 
        >will be updated
#### Info package packet: 
    "!INFO + [info]"
#### Info package receive confirmation:
    "!INFO: RECEIVED"
##### Scenario:
`client` gửi info cho `server` thông qua địa chỉ đã được quy định ngay đợt connect đầu tiên, từ đây `client` cứ hết interval sẽ gửi thông tin về cho server, nếu `server` nhận được thì `server` trả confirmation về cho `client`, không được thì thôi.
#### Disconnecting packet:
    "!DISC"
#### Disconnection package receive confirmation:
    "!DISC: RECEIVED"    
##### Scenario:
`client` gửi disconnect message cho `server` thông qua địa chỉ đã được quy định ngay đợt connect đầu tiên, `server` khi nhận được sẽ gửi gói tin confirmation về cho `client` báo việc disconnect là an toàn. 
- Trường hợp `client` không nhận được gói tin disconnection confirm từ `server` thì sau 10s sẽ gửi lại 1 lần, chờ tới khi nào `server` confirm thì mới được disconnect.
- Trường hợp `server` không thể nhận gói tin mà `client` gửi về (`server` chết hay sụp) thì python nó raise error lên để catch, khi error có thể disconnect hẳn.
  
#### Change message (server side)
    "!UPDT + [change]"
#### Change message confirmation (client will send this)
    "!UDPT: RECEIVED"
##### Scenario:
`server` gửi update message cho `client` (hiện tại mới chỉ specify cho 1 client) thông qua địa chỉ đã được quy định ngay đợt connect đầu tiên, `client` khi nhận được sẽ phải gửi một gói tin confirm về cho `server` báo nhận tin update thành công, `server` update thông tin `interval` time của client.
- Trường hợp `client` không nhận được gói tin update message từ `server` (`server` không nhận được confirmation, confirmation gửi qua TCP nên bảo đảm gửi lại tự động) thì sau 10s sẽ gửi lại 1 lần, chờ tới khi nào `client` confirm thì mới không gửi nữa.
- Trường hợp `server` không thể nhận gói tin mà `client` gửi về (`server` chết hay sụp) thì python nó raise error lên để `client` catch, khi error `client` có thể disconnect hẳn.




#### Client's sending data:
- CPU temp, Disk drive's usage, RAM's usage
```
    CPU temp: using psutil (linux), using WMI and OpenHardwareMonitor (windows)
    Disk drive's usage: using psutil
    RAM's usage: using psutil
```
- Header (indicating the length of the data): 16 bytes
- Command abbriviate: 5 bytes 
- Length of the sending data is no longer than 235 bytes
    
> Currently working on it, if there are any changes feel free to inform me and edit the code if necessary, also please update the `CHANGELOG.md` file too!