function ajaxSend(reqUest_url, post_data, callback, request_method, return_type, dict_vars) {
    var params = {
    url: reqUest_url,
    data: post_data || '',
    type: request_method || 'GET',
    success: callback,
    error: function (request, textStatus, errorThrown) {
        alert("Request failed, please try again.");
    },
    return_type: return_type || 'json',
    cache: false,
    global: true,
    ajax_func_flag: false,
    custom_func: callback
    };
    if (dict_vars) {
        for (var key in dict_vars) {
            params[key] = dict_vars[key];
        }
    }
    $.ajax(params);
}

function createTable(headData, bodyData) {
  var htmlBuffer = [];
  htmlBuffer.push("<table class='table table-strip table-bordered monitor_table'>");
  // for header
  htmlBuffer.push("<thead>\n<tr>");
  for(var i = 0; i < headData.length; i++){
      htmlBuffer.push("<th>" + headData[i] + "</th>");
  }
  htmlBuffer.push("</tr>\n</thead>");
  // for body
  htmlBuffer.push("<tbody>");
  for(var i = 0; i < bodyData.length; i++){
    htmlBuffer.push("<tr>");
    for(var j = 0; j < bodyData[i].length; j++){
        htmlBuffer.push("<td>" + bodyData[i][j] + "</td>");
        }
    htmlBuffer.push("</tr>")
  }
  htmlBuffer.push("</tbody>");
  htmlBuffer.push("</table>");
  tableStr = htmlBuffer.join('\n');
  return tableStr;
}

function createTable2(headData, bodyData, colorArray) {
  var htmlBuffer = [];
  htmlBuffer.push("<table class='table table-strip table-bordered'>");
  // for header
  htmlBuffer.push("<thead>\n<tr>");
  for(var i = 0; i < headData.length; i++){
      htmlBuffer.push("<th>" + headData[i] + "</th>");
  }
  htmlBuffer.push("</tr>\n</thead>");
  // for body
  htmlBuffer.push("<tbody>");
  for(var i = 0; i < bodyData.length; i++){
    htmlBuffer.push("<tr>");
    for(var j = 0; j < bodyData[i].length; j++){
        if(colorArray[i] != ''){
            htmlBuffer.push("<td style='color:" + colorArray[i] + "'>" + bodyData[i][j] + "</td>");
        }else{
            htmlBuffer.push("<td>" + bodyData[i][j] + "</td>");
        }
    }
    htmlBuffer.push("</tr>")
  }
  htmlBuffer.push("</tbody>");
  htmlBuffer.push("</table>");
  tableStr = htmlBuffer.join('\n');
  return tableStr;
}

// only for one excel and one sheet type
function handleFile(obj) {
    if(!obj.files){
        return;
    }
    var info = obj.files[0];
    var reader = new FileReader();
    reader.onload = function(e){
        var data = e.target.result;
        var workbook = XLSX.read(data, {type: 'binary'});
        var result = XLSX.utils.sheet_to_json(workbook.Sheets['Sheet1']);
    };
    reader.readAsBinaryString(info);
}

// django crsf token
 //Django Ajax CSRF 认证
    jQuery(document).ajaxSend(function (event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });