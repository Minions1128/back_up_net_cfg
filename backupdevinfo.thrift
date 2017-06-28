
service BackupDevInfo {
    string _login(1:string username, 2:string password)
    string get_all_dev_info()
    string add_dirfile()
    string send_mail()
    string _close()
}
