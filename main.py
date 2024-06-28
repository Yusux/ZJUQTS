from utils.alt import ALT
from getpass import getpass

username = input('Username: ')
password = getpass('Password: ')

alt = ALT(username, password)

try:
    alt.login()
    print('Login successfully')
    # traverse all the courses that need to be evaluated
    while todo_courses := alt.get_todo_courses_list():
        # {course_id: {group_id: '', form_id: '', teacher_list: [tea_sid]}}
        # store the group_id, form_id, and teacher_list of each course
        courses = {x['id']:{} for x in todo_courses['data']['data']}
        if not courses:
            break
        for course_id in list(courses.keys()):
            # get the group_id and teacher_list of the course
            course_info = alt.find_plan_course(course_id)
            group_id = course_info['data']['groupId']
            teacher_list = [x['userSid'] for x in course_info['data']['teacherList']]
            courses[course_id]['group_id'] = group_id
            courses[course_id]['teacher_list'] = teacher_list
            # create a form for the course
            form = alt.insert_document(group_id)
            courses[course_id]['form_id'] = form['data']
            # evaluate the course for each teacher teaching the course
            for tea_sid in teacher_list:
                eval_res = alt.save_plan_course(course_id, form['data'], tea_sid)
except Exception as e:
    print(e)

print('All courses have been evaluated')