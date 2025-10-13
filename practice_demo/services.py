from practice_demo.models import Student, DataResponse

def get_data() -> DataResponse:
    return DataResponse(
        students=[
            Student(name="Sai", age=22),
            Student(name="Kiran", age=23)
        ],
        position=(12.5, 45.6)
    )
