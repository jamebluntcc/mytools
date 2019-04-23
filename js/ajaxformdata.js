$(document).ready(function(){
  $('#vcf-sub').click(function(){
    var formData = new FormData();
    var vcf_type = $("#vcf-type").find("option:selected").text();
    formData.append("vcf_type", vcf_type);
    formData.append("vcf_file", document.getElementById('vcf-file').files[0]);
    $.ajax({
      url: "/upload/",
      type: "POST",
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        if (data.msg == "ok") {
            alert("upload success");
        }else{
          alert(data.msg);
        }}
    });
  });
});
