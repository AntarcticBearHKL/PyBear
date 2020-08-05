window.onload = function(){
    window.onresize()

    var vue = new Vue({
        el: '#Context',
        data: {
            WebDisk_FileTable_Data: [],
            WebDisk_UploadDialog_Visible: false,
            WebDisk_NewDierctoryDialog_Visible: false,
            WebDisk_NewDierctoryDialog_Input: '',
            WebDisk_UploadArea_Para: {
                'Command': 'Upload',
                'Url': '',
            }
        },
        methods: {
            UserLogin: function(){
                this.$http.post('/Personal', {'Command':'Login'}).then(function(res){
                    switch(res.body){
                        case 'AU_Authentication_Failed':
                            window.location.href="/Login"
                            break;
                        case 'AU_Authentication_Expire':
                            window.location.href="/Login"
                            break;
                        default:
                            ID('Profile_Avater').innerHTML = res.body
                    }
                },function(){
                    alert('登录请求失败')
                    window.location.href="/Login";
                });
            },

            SideBar_Menu_Select: function(index){
                ID('Diary').style.display = 'none'
                ID('Plan').style.display = 'none'
                ID('Financial').style.display = 'none'
                ID('Idea').style.display = 'none'
                ID('Information').style.display = 'none'
                ID('WebDisk').style.display = 'none'
                ID('Setting').style.display = 'none'
                if(index==1){
                    ID('Diary').style.display = 'block'
                }
                else if(index==2){
                    ID('Plan').style.display = 'block'
                }
                else if(index==3){
                    ID('Financial').style.display = 'block'
                }
                else if(index==4){
                    ID('Idea').style.display = 'block'
                }
                else if(index==5){
                    ID('Information').style.display = 'block'
                }
                else if(index==6){
                    ID('WebDisk').style.display = 'block'
                    bp.WD_Path = '/'
                    vue.WebDisk_listDir()
                }
                else if(index==7){
                    ID('Setting').style.display = 'block'
                }
            },

            WebDisk_listDir: function(){
                this.WebDisk_FileTable_Data = []
                this.$http.post('/Personal', {'Command':'ListDir', 'Url':bp.WD_Path}).then(function(res){
                    for(var item in res.body){
                        if (res.body[item][0] == 'directory'){
                            res.body[item][1] = 'Directory'
                        }
                        info = {
                            name: item,
                            size: res.body[item][1],
                            changeDate: res.body[item][2],
                        }
                        this.WebDisk_FileTable_Data.push(info)
                    }
                },function(){
                    alert('获取路径失败')
                    window.location.href="/Login";
                });

                this.WebDisk_UploadArea_Para.Url = bp.WD_Path

                var parent = ID('WebDisk_NaviBar_Breadcrumb')
                cm.DropAllChild(parent)
                var path = bp.WD_Path.split('/')

                LeftOffset = 30
                LeftSpace = 5

                for(var i=0; i<path.length-1; i++){
                    if(i==0){
                        LeftOffset = 30

                        var child = cm.NewNode('el-button')
                        if (path.length-1>1){
                            child.classList.add('WebDisk_NaviBar_Item')
                            child.onclick = function(){
                                bp.WD_Path = '/'
                                vue.WebDisk_UploadArea_Para.Url = bp.WD_Path
                                vue.WebDisk_listDir()
                            }
                        }
                        else{
                            child.classList.add('WebDisk_NaviBar_Item_Last')
                        }
                        child.innerHTML = '首页'

                        child.style.left = (LeftOffset).toString() + 'px'
                        cm.AppendNode(parent, child, null)
                        LeftOffset = LeftOffset + parseInt(child.clientWidth)
                    }
                    else{
                        var spliter = cm.NewNode('p')
                        spliter.classList.add('WebDisk_NaviBar_Item_split')
                        spliter.innerHTML = ' > '

                        spliter.style.left = (LeftOffset + LeftSpace).toString() + 'px'
                        cm.AppendNode(parent, spliter, null)
                        LeftOffset = LeftOffset + LeftSpace + parseInt(spliter.clientWidth)

                        var child = cm.NewNode('el-button')
        
                        if (i==path.length-2){
                            child.classList.add('WebDisk_NaviBar_Item_Last')
                        }
                        else{
                            child.classList.add('WebDisk_NaviBar_Item')
                            child.onclick = function(){
                                TempPath = []
                                for (var c=0; c<i-1; c++){
                                    TempPath.push(path[c])
                                }
                                TempPath.push('')
                                bp.WD_Path = TempPath.join('/')
                                vue.WebDisk_UploadArea_Para.Url = bp.WD_Path
                                vue.WebDisk_listDir()
                            }
                        }
                        child.innerHTML = path[i]

                        child.style.left = (LeftOffset + LeftSpace).toString() + 'px'
                        cm.AppendNode(parent, child, null)
                        LeftOffset = LeftOffset + LeftSpace + parseInt(child.clientWidth)
                    }
                }
            },
            WebDisk_FileTable_Click: function(row, column, event){
                this.$refs.WebDisk_FileTable_Ref.toggleRowSelection(row)
            }, 
            WebDisk_FileTable_DoubleClick: function(row, column, event){
                if(row.size=='Directory'){
                    bp.WD_Path = bp.WD_Path + row.name + "/"
                    this.WebDisk_listDir()
                }
            },
            WebDisk_UploadDialog_Closed: function(){
                this.$refs.WebDisk_UploadArea_Ref.clearFiles()
                this.WebDisk_listDir()
            },
            WebDisk_ToolsBar_AddDirectory: function(){
                this.$http.post('/Personal', {'Command':'NewDir', 'DirectoryName': WebDisk_NewDierctoryDialog_Input,'Url':bp.WD_Path}).then(function(res){
                    console.log(res.body)
                },function(){
                    alert('登录请求失败')
                    window.location.href="/Login";
                });
            },
            WebDisk_ToolsBar_Download_Click: function(){
                
            },
        }
    })

    vue.UserLogin()

    bp.WD_Path= '/'
}

window.onresize = function(){
    wwidth = ID('Background').clientWidth
    wheight = ID('Background').clientHeight

    ID('SideBar').style.height = wheight - 150 + 'px'

    ID('Panel').style.height = wheight - 40 + 'px'
    ID('Panel').style.width = wwidth - 330 + 'px'
    ID('Panel').style.top = '20px'
    ID('Panel').style.left = '300px'

    ID('WebDisk_FileTable').style.height = (parseInt(ID('Panel').style.height) - 140) + 'px'
}