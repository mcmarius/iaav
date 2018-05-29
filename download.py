from requests import get as r_get
#import shutil

page = 'http://www.doreltopan.com/gallery/'
an_start = 2012
an_end = 2013
fill = '/00'


def save_pics(path):
    for an in range(an_start, an_end+1):
        filler = fill
        pic = 1
        while 1:
            if pic > 9:
                break
                filler = '/01'
                pic -= 9
            request = r_get(page + str(an) + filler + str(pic) + '.jpg', stream=True)
            cod = request.content[0]
            if cod == 60 and request.content[1] == 33:
                break
            pic += 1
            with open(path + '/' + str(an) + '_' + filler[2] + str(pic) + '.jpg', 'wb') as f:
                #request.raw.decode_content = True
                #shutil.copyfileobj(request.raw, f)
                f.write(request.content)


def save_pic_1(path):
    for an in range(an_start, an_end+1):
        request = r_get(page + str(an) + '/011.jpg', stream=True)
        cod = request.content[0]
        if cod == 60 and request.content[1] == 33:
            break
        with open(path + '/' + str(an) + '_011.jpg', 'wb') as f:
            f.write(request.content)


if __name__ == '__main__':
    save_pics('/home/marius/Documents/anul_III/sem_II/arte/proiect/topan')
