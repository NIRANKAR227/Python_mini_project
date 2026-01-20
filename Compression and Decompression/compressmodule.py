import base64,zlib

def compress(inputfile,outputfile):
    data=open(inputfile,'r').read()
    data_bytes=bytes(data,'utf-8')
    compressed_data= base64.b64encode(zlib.compress(data_bytes,9))   # As .compress() only write byte data 

    compressed_file=open(outputfile,'w')
    decoded_data=compressed_data.decode('utf-8')  # As .decode() function only write string data to file
    compressed_file.write(decoded_data)

def decompress(inputfile,outputfile):
    file_content=open(inputfile,'r').read()
    encoded_data=file_content.encode('utf-8')  # Here encoding is required as the encoding formaat for a document must be known system
    decompress_data=zlib.decompress(base64.b64decode(encoded_data))
    decoded_data=decompress_data.decode('utf-8')
    file=open(outputfile,'w')
    file.write(decoded_data)
    file.close()

compress('demo.txt','ot_compress.txt')
decompress('ot_compress.txt','decompressed_demo.txt')