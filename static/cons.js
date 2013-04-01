$(document).ready(function(){
    var console2 = $('<div class="console2">');
    $('.feed').append(console2);
    controller2 = console2.console({
        promptLabel: '> ',
        commandValidate:function(line){
            if (line == "") return false;
            else return true;
        },
        commandHandle:function(line){
            // var self = this;
            $.ajax( {url: "trussvis", 
                    type:"POST", 
                    contentType:"text/plain",
                    dataType:"json",
                    data: JSON.stringify({'line':line}),
                    success: function(data){
                        controller2.commandResult(data['msg']);
                        state = data;
                        redraw();
                        },
                    error:function(a,b,c){console.log("FAILED"+c)}});

            // try { var ret = eval(line);
            //     if (typeof ret != 'undefined') return ret.toString();
            //     else return true; }
            // catch (e) { return e.toString(); }
        },
        animateScroll:true,
        promptHistory:true,
        welcomeMessage:'Welcome to TrussViz.'
    });
    controller2.promptText('load test.json');
});

send = function(s){
    $.ajax( {url: "trussvis", 
        type:"POST", 
        contentType:"text/plain",
        dataType:"json",
        data: JSON.stringify({'line':s}),
        success: function(data){
            console.log(data['msg']);
            state = data;
            redraw();
            },
        error:function(a,b,c){console.log("FAILED"+c)}});
} 