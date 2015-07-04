- GoodbyeCy (싸이월드 사진첩 백업과 티스토리/이글루스/텍스트큐브 이전)

 - Blog: http://morcavon.com/1178440402

 - 개발환경: Windows7, Python 2.7, wxPython, PyQt4, autopy, spynner (UI 편집은 Boa Constructor 필요)

 - 2015.07.03 현재 로그인 및 사진 백업 기능 문제 없음. (블로그 마이그레이션 기능은 확인 못 함)






**** windows binary 생성시 유의 사항
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