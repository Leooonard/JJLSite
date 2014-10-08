


(function(w, d, s){
    var window= w;
    var document= d;
    var screen= s;

    /*调用顺序.
    1. initArgs
    2. addListener
    3. setSuccessCallback
    4. setErrorCallback
    5. setProgressCallback*/


    var UploadHelper= function(){
        // size -1表示不限制文件大小.
        var size= -1;
        var type= 'all';
        var suffixArray= undefined;
        var showcaseImg= undefined;
        // useable决定了是否可以用附加功能, 基础功能可以使用.
        if(window.FileReader){
            var useable= true;
            var reader= new FileReader();
        }else{
            var useable= false;
        }
        this.initArgs= function(dict){
            size= dict['size']|| -1;
            type= dict['type']|| 'all';
            suffixArray= dict['suffixArray']|| new Array();
            showcaseImg= dict['showcaseImg']|| undefined;
        };

        var errorCallback= undefined;
        this.setErrorCallback= function(callback){
            errorCallback= callback|| function(error){};
        }

        var successCallback= undefined;
        this.setSuccessCallback= function(callback){
            successCallback= callback|| function(success){};
        };

        var progressCallback= undefined;
        this.setProgressCallback= function(callback){
            progressCallback= callback|| function(progress){};
        };

        this.addListener= function(input){
            // 判断是否为jquery对象.
            if(input instanceof jQuery){
                input= input[0];
            }
            // 这种形式定义的函数一定要再使用前出现!!!
            var readFile= function(e){
                var event= e|| window.event;
                // 是files不是file!!!!
                if(useable){
                    var file= this.files[0];
                    var typeReg= new RegExp(type+ '\/[a-z]+');
                    var sizeThreshold= size;
                    if(type!= 'all'&& !typeReg.test(file.type)){
                        errorCallback("文件类型错误, 请上传"+ type+ "类型文件.");
                        return;
                    }
                    if((size!= -1)&& (parseInt(file.size)> size)){
                        errorCallback('文件大小超过限制');
                        return;
                    }

                    reader.onload= function(e){
                        var event= e|| window.event;
                        var src= this.result;
                        if(type== 'image' && showcaseImg){
                            $(showcaseImg).attr('src', src);
                            $(showcaseImg).css('height', 'auto');
                        }
                    };
                    /*reader.onprogress= function(e){
                        var event= e|| window.event;
                        var progress= parseInt(event.loaded/ event.total* 100);
                        progressCallback(progress);
                    };*/

                    // 读取文件的函数.
                    reader.readAsDataURL(file);
                }else{
                    alert('浏览器不支持上传预览!');
                    var src= event.target|| event.srcElement;
                    var file= {
                        name: src.value
                    }
                }
                // 后缀检测.
                var suffixReg= new Array();
                for(var i= 0; i< suffixArray.length; i++){
                    suffixReg.push(new RegExp('\.'+ suffixArray[i]+ '$'));
                }
                if(suffixReg.length> 0){                 
                    try{              
                        for(var i= 0; i< suffixReg.length+ 1; i++){
                            if(suffixReg[i].test(file.name)){
                                break;
                            }
                        }
                    }catch(e){
                        var errorStr= '文件后缀错误, 请上传后缀为';
                        for(var i= 0; i< suffixArray.length; i++){
                            errorStr+= suffixArray[i]+ ', ';
                        }
                        errorStr= errorStr.slice(0, errorStr.length- 2);
                        errorStr+= '的文件';
                        errorCallback(errorStr);
                        return;
                    }
                }

                successCallback('文件可以上传');

            };
            if(input.addEventListener){
                input.addEventListener('change', readFile, false)
            }else{
                input.attachEvent('onchange', readFile);
            }
        };
    };

    window['UploadHelper']= UploadHelper;
})(window, document, screen);