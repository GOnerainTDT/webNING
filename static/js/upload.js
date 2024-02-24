function previewAndUploadImage(event) {
    console.log("previewAndUploadImage function triggered");
    var file = event.target.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var output = document.querySelector('.image.fit img');
            if(output) {
                output.src = e.target.result;
            }

            var formData = new FormData();
            formData.append('fileInput', file);

            console.log("Sending file to server:", file);

            fetch('/upload_image', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('currentTime').innerHTML = data.strFortune;
                } else {
                    document.getElementById('currentTime').innerHTML = data.message + "<br>当前时间: " + data.current_time + "<br>city: " + data.city;
                }
            })
            .catch(error => {
                console.error('Error during fetch:', error);
            });
        };
        reader.readAsDataURL(file);
    }
}


// function previewAndUploadImage(event) {
//     var file = event.target.files[0];
//     if (file) {
//         var reader = new FileReader();
//         reader.onload = function(e) {
//             // 预览图片
//             var output = document.querySelector('.image.fit img');
//             output.src = e.target.result;

//             // 显示当前时间
//             var now = new Date();
//             var currentTimeText = now.toLocaleString(); // 获取当前时间的字符串表示
//             document.getElementById('currentTime').innerText = "当前时间: " + currentTimeText;

//             // 创建 FormData 对象并附加文件
//             var formData = new FormData();
//             formData.append('fileInput', file);

//             // 发送 POST 请求到服务器上传图片
//             fetch('/upload_image', {
//                 method: 'POST',
//                 body: formData,
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.text();
//             })
//             .then(data => {
//                 console.log(data);
//                 // 这里可以添加更多的前端逻辑，例如显示上传成功消息
//             })
//             .catch(error => {
//                 console.error('Error during fetch:', error);
//             });
//         };
//         reader.readAsDataURL(file);
//     }
// }

// // function previewAndUploadImage(event) {
// //     var file = event.target.files[0];
// //     if (file) {
// //         var reader = new FileReader();
// //         reader.onload = function(e) {
// //             // 预览图片
// //             var output = document.querySelector('.image.fit img');
// //             output.src = e.target.result;

// //             // 创建 FormData 对象并附加文件
// //             var formData = new FormData();
// //             formData.append('fileInput', file);

// //             // 发送 POST 请求到服务器上传图片
// //             fetch('/upload_image', {
// //                 method: 'POST',
// //                 body: formData,
// //             })
// //             .then(response => {
// //                 if (!response.ok) {
// //                     throw new Error('Network response was not ok');
// //                 }
// //                 return response.text();
// //             })
// //             .then(data => {
// //                 console.log(data);
// //                 // 这里可以添加更多的前端逻辑，例如显示上传成功消息
// //             })
// //             .catch(error => {
// //                 console.error('Error during fetch:', error);
// //             });
// //         };
// //         reader.readAsDataURL(file);
// //     }
// // }