# Develop Guide for HOYA AI
### Git Guide 
 - Commit 주기는 기능이 완성된 상태에서 할 것(빌드나 동작의 완성 상태)
 - 한줄로 간결하게 요약 끝에는 마침표(.)을 찍지 않음
 - 제목 첫글자는 대문자로 쓸것
 - 무엇을 왜 했는지만 쓰면됨 (어떻게는 쓸필요없음 - 코드로 확인가능)
 
[Commit Message Example]
 - "[동사] + [목적어] + [보어]"
 - "[행위] + [대상] + [사유]"
 - "Modify CNN parameter for train"
 - "Add new class to make node"
 - "Fix the bug returns a type error"
 - "Merge workflow neuralnet_node to add function"

Frequently Use Command 
```sh
$ git status
$ git pull -r
 ```
Git flow is (Modified -> Staged(ADD) -> Commit)
 ```sh
$ git add "파일명"
$ git commit -m "내용"
$ git push
  ```
Set Global PATH
```sh
$ git config --global user.namenode "ID" 
$ git config --global user.email "ID@XXX.XXX"
```
Cancel PUSH
```sh
$ git push -f origin (last commit id):master
```
Local RESET
```sh
$ git fetch origin
$ git reset --hard origin/master
```
Fix conflict (After pull and pop)
```sh
$ git stash
$ git stash pop 
```


### Mark Down Guide
* [Mark Down Editor] (http://dillinger.io) - Online Guide
