

class TaskManager:

    def serviceCall(self, intend, entity) : #parm = {"type" : "", "result" : []}) :

        try:
            print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 6) 서비스 호출")
            print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 서비스 호출 파라미터 의도 출력 {0}".format(intend))
            print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆ 서비스 호출 파라미터 속성 출력 {0}".format(entity))

            return None
        except Exception as e:
            raise Exception(e)