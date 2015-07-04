
 - GoodbyeCy (싸이월드 사진첩 백업과 티스토리/이글루스/텍스트큐브 이전)

 - Blog: http://morcavon.com/1178440402

 - 개발환경: Windows7, Python 2.7, wxPython, PyQt4, autopy, spynner (UI 편집은 Boa Constructor 필요)



* windows binary 생성시 유의 사항
spynner 패키지에 있는 browser.py 수정이 필요함

아래 부분을

```
#!python

    _javascript_directories = [
        pkg_resources.resource_filename('spynner', 'javascript'),
    ]
```


이렇게 수정해야 함

```
#!python

    _javascript_directories = [
        'javascript',
    ]
```