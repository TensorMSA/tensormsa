$(document).ready(function() {
    myBotApp.initialize();
    myBotApp.start();
});
//화면에서 넘어온 Chatbot ID 매핑
var parameters = location.search.substring(1).split("?");
var temp = parameters[0].split("=");

var myBotApp = {
    ajaxServiceUrl: location.origin,
    ajaxRequestMessageMethod: "PUT",
    ajaxRequestMessageApiPath: "/api/v1/type/service/chatbot/" + temp[1] + "/",
    fileTranferImageUploadApiPath: "/",
    langMap: {
        headerTitle: "AI 테스트봇",
        startMsg : "안녕하세요, 테스트봇입니다.<br>무엇을 도와드릴까요?",
        textNotUnderstandMsg : "무슨 말씀인지 이해할 수 없어요.",
        imageNotUnderstandMsg : "무슨 사진인지 이해할 수 없어요.",
        apiCallErrorMsg : "서버 요청에 실패했어요. ㅠㅠ",
        apiCallEmptyResultMsg : "서버 응답에 내용이 없네요? ;;;",
        showDetailInfoBtn : "상세보기",
        hideDetailInfoBtn : "감추기"
    },
    bufferResponseMsg: {

        intent_id : "",
        edit_history : [],
        input_data : "",
        convert_data : "",
        intent_history : [],
        request_type : "text",
        service_type : "",
        story_board_id : "",
        story_key_entity : [],
        story_slot_entity : {},
        output_data : ""    

    },
    initialize: function() {
        var me = this;

        $("#chatBotHeaderTitle").html(me.langMap.headerTitle + " - " + me.ajaxServiceUrl);

        $("#inputMessage").keypress(function( event ) {
            if ( event.which == 13 ) {
                me.sendMessage();
                event.preventDefault();
            }
        });

        $("#albumPicture").click(function() {
            me.cordovaCamera(Camera.PictureSourceType.SAVEDPHOTOALBUM);
            return false;
        });

        $("#takePicture").click(function() {
            me.cordovaCamera(Camera.PictureSourceType.CAMERA);
            return false;
        });

        $("#sendMessage").click(function() {
            me.sendMessage();
            return false;
        });
    },
    start: function() {
        var me = this;

        // BOT START MESSAGE
        innerHTML = $("<div>").addClass("messageRow");
        innerHTML.append($("<div>").addClass("profilePicture"));
        var innerElement = innerHTML.append($("<span>").addClass("otherMessage").html(me.langMap.startMsg));
        $("#chatBotWindowMain").append(innerHTML);
        $("#chatBotWindowMain").scrollTop($("#chatBotWindowMain").prop("scrollHeight"));
    },
    cordovaCamera: function(srcType) {
        var me = this;
        var options = {
            quality: 100,
            destinationType: Camera.DestinationType.DATA_URL,
            sourceType: srcType,
            encodingType: Camera.EncodingType.PNG,
            mediaType: Camera.MediaType.PICTURE,
            allowEdit: true,
            correctOrientation: true,
            targetWidth : 200,
            targetHeight : 320
        };
        navigator.camera.getPicture(function cameraSuccess(imageUri) {
            me.sendImage(imageUri);
        }, function cameraError(error) {
            console.debug("Unable to obtain picture: " + error, "app");
        }, options);
    },
    cordovaFileTranfer: function(imageUri) {
        var me = this;
        var options = new FileUploadOptions();

        options.fileKey="file";
        options.fileName=imageUri.substr(imageUri.lastIndexOf('/')+1);
        options.mimeType="text/plain";

        var headers = {'headerParam':'headerValue'};
        options.headers = headers;

        var ft = new FileTransfer();
        ft.onprogress = function(progressEvent) {
            if (progressEvent.lengthComputable) {
                loadingStatus.setPercentage(progressEvent.loaded / progressEvent.total);
            } else {
                loadingStatus.increment();
            }
        };

        ft.upload(
            imageUri,
            encodeURI(me.ajaxServiceUrl +  me.fileTranferImageUploadApiPath),
            function win(r) {
                console.log("Code = " + r.responseCode);
                console.log("Response = " + r.response);
                console.log("Sent = " + r.bytesSent);

                var retData = eval("(" + r.response + ")");

                innerElement.find(".otherMessageLoading").remove();
                innerElement.find(".otherMessage").css("width", "calc(100% - 100px)");
                innerElement.find(".otherMessage").html(CreateDetailView(retData)).show();

                $("#chatBotWindowMain").scrollTop($("#chatBotWindowMain").prop("scrollHeight"));
            },
            function fail(error) {
                console.log("An error has occurred: Code = " + error.code);
                console.log("upload error source " + error.source);
                console.log("upload error target " + error.target);

                innerElement.find(".otherMessageLoading").remove();
                innerElement.find(".otherMessage").html(me.langMap.apiCallErrorMsg).show();

                $("#chatBotWindowMain").scrollTop($("#chatBotWindowMain").prop("scrollHeight"));
            },
            options
        );
    },
    sendMessage: function() {
        var me = this;
        var msg = $("#inputMessage").val();

        if(msg.length == 0) return;

        // MY MESSAGE : LOCAL
        var innerHTML = $("<div>").addClass("messageRow");
        innerHTML.append($("<span>").addClass("myMessage").html(msg));
        $("#chatBotWindowMain").append(innerHTML);

        // BOT MESSAGE : AJAX
        innerHTML = $("<div>").addClass("messageRow");
        innerHTML.append($("<div>").addClass("profilePicture"));
        innerHTML.append($("<div>").addClass("otherMessageLoading").show());
        var innerElement = innerHTML.append($("<span>").addClass("otherMessage").hide());
        $("#chatBotWindowMain").append(innerHTML);
        $("#chatBotWindowMain").scrollTop($("#chatBotWindowMain").prop("scrollHeight"));

        me.messageRequest(innerElement, "text", msg);
        $("#inputMessage").val("");
    },
    sendImage: function(imageUrl) {
        var me = this;

        // MY MESSAGE : LOCAL
        innerHTML = $("<div>").addClass("messageRow");
        innerHTML.append($("<div>").addClass("myPicture").css("background", "url(data:image/png;base64," + imageUrl + ")"));
        $("#chatBotWindowMain").append(innerHTML);
        $("#chatBotWindowMain").scrollTop($("#chatBotWindowMain").prop("scrollHeight"));

        // BOT MESSAGE : File Tranfer
        innerHTML = $("<div>").addClass("messageRow");
        innerHTML.append($("<div>").addClass("profilePicture"));
        innerHTML.append($("<div>").addClass("otherMessageLoading").show());
        var innerElement = innerHTML.append($("<span>").addClass("otherMessage").hide());
        $("#chatBotWindowMain").append(innerHTML);
        $("#chatBotWindowMain").scrollTop($("#chatBotWindowMain").prop("scrollHeight"));

        me.messageRequest(innerElement, "image", imageUrl);
    },
    messageRequest: function(innerElement, hoyaiRequestType, inputData) {
        var me = this;

        var tempMessage = me.bufferResponseMsg;
        tempMessage.request_type = hoyaiRequestType;
        tempMessage.input_data = inputData;
        tempMessage.output_data = "";
        console.log(tempMessage)

        var params = JSON.stringify(tempMessage);
        $.ajax({
            type: me.ajaxRequestMessageMethod,
            url: me.ajaxServiceUrl + me.ajaxRequestMessageApiPath,
            contentType : "application/json",
            timeout: 50000,
            async: true,
            data: params,
            success: function (data, status, jqXhr) {
                var retData = data;
                console.log("Debug Chat");
                console.log(data);
                //var retData = JSON.parse(data);
                if(typeof retData != 'object') retData = JSON.parse(eval(data));

                me.bufferResponseMsg = retData;

                innerElement.find(".otherMessageLoading").remove();
                console.log(retData);
                var btnDetailInfo = $("<button>").addClass("btnDetailInfo").html(me.langMap.showDetailInfoBtn);
                innerElement.find(".otherMessage").html((typeof retData.output_data != 'undefined' && retData.output_data.length > 0 ? retData.output_data : me.langMap.apiCallEmptyResultMsg)).append(btnDetailInfo).show();

                btnDetailInfo.click(function() {
                    var detailObj = $(this).next();
                    if(detailObj.is(":visible") == true) {
                        $(this).html(me.langMap.showDetailInfoBtn);
                        innerElement.find(".otherMessage").css("width", "initial");
                        detailObj.hide();
                    } else {
                        $(this).html(me.langMap.hideDetailInfoBtn);
                        innerElement.find(".otherMessage").css("width", "calc(100% - 100px)");
                        detailObj.show();
                    }

                    return false;
                });

                innerElement.find(".otherMessage").append($("<div>").addClass("detailInfo").html(CreateDetailView(retData)));

                $("#chatBotWindowMain").scrollTop($("#chatBotWindowMain").prop("scrollHeight"));
            },
            error: function (jqXhr, textStatus, errorMessage) {
                innerElement.find(".otherMessageLoading").remove();
                innerElement.find(".otherMessage").html(me.langMap.apiCallErrorMsg).show();

                $("#chatBotWindowMain").scrollTop($("#chatBotWindowMain").prop("scrollHeight"));
            }
        });
    }
};

/* 원본소스 : http://www.zachhunter.com's CreateDetailView Function
 * 오류수정 : typeof objArray === 'string'일 경우 아래 라인에서 파싱 오류가 발생하므로 체크하여 바로 리턴되도록 처리
 */
function CreateDetailView(objArray, theme, enableHeader) {
    // set optional theme parameter
    if (theme === undefined) theme = 'chatbotResult';  //default theme
    if (enableHeader === undefined) enableHeader = true; //default enable headers

    // 오류수정 : typeof objArray === 'string'일 경우 아래 라인에서 파싱 오류가 발생하므로 체크하여 바로 리턴되도록 처리
    if(typeof objArray === 'string') return objArray;

    var array = typeof objArray != 'object' ? JSON.parse(objArray) : new Array(objArray);
    var keys = Object.keys(array[0]);
    var str = '<table class="' + theme + '">';
    str += '<tbody>';

    for (var i = 0; i < array.length; i++) {
        var row = 0;
        for (var index in keys) {
            var objValue = array[i][keys[index]]

            str += (row % 2 == 0) ? '<tr class="alt">' : '<tr>';
            if (enableHeader) str += '<th scope="row">' + keys[index] + '</th>';

            // Support for Nested Tables
            if (typeof objValue === 'object' && objValue !== null) {
                if (Array.isArray(objValue)) {
                    str += '<td>';
                    for (var aindex in objValue) str += CreateDetailView(objValue[aindex], theme, true);
                    str += '</td>';
                } else {
                    str += '<td>' + CreateDetailView(objValue, theme, true) + '</td>';
                }
            } else {
                str += '<td>' + (objValue.indexOf("iVBO") == 0 ? "<img class='resultImage' src='data:image/png;base64," + objValue + "'>" : objValue) + '</td>';
            }

            str += '</tr>';
            row++;
        }
    }

    str += '</tbody>'
    str += '</table>';
    return str;
}

function onBackKeyDown() {
    console.log("BackKey Pressed!");
}
