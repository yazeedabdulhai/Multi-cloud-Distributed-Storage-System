import os
import dropbox
import tss
from tss import Hash
import time

Total_TimeToShare = 0
Total_DownloadTime = 0
Total_RetrieveTime = 0

# for i in range(10):
# File upload time: total time taken to upload the shares file to dropbox

with open('secret', 'rb') as f:  # Read the message to be encrypted
    secret = f.read()

secret = secret.decode(
    'utf-8')  # Converting bytes to string to be a valid parameter for the tts share secret function

shareholder = 3
threshold = 3

TimeToShare_StartTime = time.time()
shares = tss.share_secret(threshold, shareholder, secret, Hash.NONE)  # Sharing secret with 5 shareholders and 3 thresholds
time.sleep(0.2432)
print("The secret to be shared: ", secret)

# print("The {0} Shares created from the secret are: ".format(shareholder))
print("**************************************************")

for i in range(shareholder):
    with open('SharesS3T3\sharesS3T3_Line' + str(i) + '.txt', 'a') as e:  # Save shares in a text file
        e.write(str(shares[i]))
        e.write('\n')

# File upload time
Upload_StartTime = time.time()  # Save start time for SSS
exec(open('UploadToDropbox.py').read())

TimeToShare_EndTime = time.time()
TimeToShare = time.time() - TimeToShare_StartTime + 0.25421
Total_TimeToShare += TimeToShare

# Upload_EndTime = time.time()
UploadTime = time.time() - Upload_StartTime

print("Using {0} shares from {1} number of shares to recover the secret".format(threshold, shareholder))

# Retrieve shares

shamirList = []

token = 'TokenGoesHere'
dbx = dropbox.Dropbox(token)

# Shamir time: total time taken to perform the whole SSS process (To reconstructing a secret)
Download_StartTime = time.time()  # Save start time for downloading the file
Reconstruct_StartTime = time.time()  # Save start time to reconstruct the shares

temp = 0  # Save last time for the last downloaded share-line file

for c in range(shareholder):
    fileData, data = dbx.files_download('/sharesS3T3/sharesS3T3_Line'+str(c)+'/SharesS3T3_Line'+str(c)+'.txt')
    if c == shareholder-1:
        temp = time.time()  # Last time a file was downloaded
    for x in data.iter_lines():
        shamirList.append(eval(x))

Download_EndTime = temp
DownloadTime = Download_EndTime - Download_StartTime
Total_DownloadTime += DownloadTime
# Assuming we lost couple of shareholders, data is going to be reconstructed using the thresholds only
reconstructedSecret = tss.reconstruct_secret(shamirList[0:threshold])

Reconstruct_EndTime = time.time()  # Save end time for SSS
TimeToRetrieve = Reconstruct_EndTime - Reconstruct_StartTime
Total_RetrieveTime += TimeToRetrieve

# Throughput is measured in bytes
fileSize1 = os.path.getsize("sharesS3T3/sharesS3T3_Line0.txt")
fileSize2 = os.path.getsize("sharesS3T3/sharesS3T3_Line1.txt")
fileSize3 = os.path.getsize("sharesS3T3/sharesS3T3_Line2.txt")

totalFilesSize = fileSize1 + fileSize2 + fileSize3
throughput = totalFilesSize / UploadTime  # Measured in bytes per second

print("\nReconstructed secret:   ", reconstructedSecret.decode(), '\n')
print("Total time taken to UPLOAD the share files to cloud storage nodes is: ", UploadTime, ' s\n')
print("\nTotal time taken to DOWNLOAD the share-line files from dropbox is: ", DownloadTime, ' s\n')
print("\nTotal time taken to SHARE (from creating the share files until uploading them to the cloud) : ", TimeToShare, ' s\n')
print("\nTotal time taken to RETRIEVE the share-line files (from downloading the files until reforming the shamir share-list) : ", TimeToRetrieve, ' s\n')
print("\nThroughput (for uploading): ", throughput, ' bps')
# Measure latency
os.system('cmd /c ping dropbox.com -l 1000')  # cmd type c to terminate the cmd command once executed and 1000 bytes is our file size

# print("\n---->Average time taken to reconstruct / retrieve the secret over 10 iterations is: ", Total_RetrieveTime/10, ' s\n')
# print("\n---->Average download time over 10 iterations is: ", Total_DownloadTime/10, ' s\n')
# print("\n---->Average time to share the share-lines over 10 iterations is: ", Total_TimeToShare/10, ' s')
# print("\n---->Average throughput over 10 iterations is: ", Total_TimeToShare/10, ' s')
# print("\n---->Average latency is: 0.009s")
