function calc_md5(file, chunkSize, form) {
    var blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice,
        chunks = Math.ceil(file.size / chunkSize),
        currentChunk = 0,
        spark = new SparkMD5.ArrayBuffer(),
        fileReader = new FileReader();
    fileReader.onload = function (e) {
        spark.append(e.target.result);                   // Append array buffer
        currentChunk++;
        if (currentChunk < chunks) {
            loadNext();
        } else {
            form['md5'].value = spark.end();
            console.log('finished loading');
            console.log('md5 = ' + form['md5'].value);
        }
    };

    fileReader.onerror = function () {
        console.warn('oops, something went wrong.');
    };

    function loadNext() {
        var start = currentChunk * chunkSize,
            end = ((start + chunkSize) >= file.size) ? file.size : start + chunkSize;
        fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
    }

    loadNext();
}
