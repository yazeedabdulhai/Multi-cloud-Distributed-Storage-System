import dropbox


class CloudStorage:
    def __init__(self, access_token):
        self.at = access_token

    def uploadFile(self, fileFrom, fileTo):
        f = open(fileFrom, 'rb')
        f = f.read()
        dbx = dropbox.Dropbox(self.at)
        if fileFrom != '' and fileTo != '':
            dbx.files_upload(f, fileTo)
            print('Share line has been uploaded to a Dropbox node successfully !')
        else:
            print('Local and dropbox file locations are required!')


def main():
    print('*** Welcome to python based dropbox cloud storage system ***\n')
    token = 'TokenGoesHere'
    user = CloudStorage(token)
    for i in range(3):
        fileFrom = r'C:\University\Cyber Security\Labs\PRES 1_TEST\SharesS3T3\sharesS3T3_Line'+str(i)+'.txt'
        fileTo = '/sharesS3T3/sharesS3T3_Line'+str(i)+'/SharesS3T3_Line'+str(i)+'.txt'
        user.uploadFile(fileFrom, fileTo)


if __name__ == '__main__':
    main()
