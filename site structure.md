.
+-- /index
    @ Main page, promotional content, registeration and login
    +-- /index
        @ For logged in users
        +-- trainee
            @ registered in courses, new courses promotions
        +-- trainer
            @ courses activity, lecture rooms promotions
        +-- training center
            @ courses activity, lecture rooms promotions
        +-- lecture room
            @ applications from trainers and training centers

+-- /user/$trainee
    @ Profile page for trainees
    +-- /user/$trainee?edit=true
        @ profile edit page

+-- /user/$trainer
    @ Profile page for trainers
    @ trianer info and links to offered courses
    +-- /user/$trainer|$center?edit=true
        @ profile edit page

+-- /user/$training_center
    @ Profile page for training centers
    @ training center info and links to offered courses/trainers
    +-- /user/$center?edit=true
        @ profile edit page

+-- /user/$lecture_room
    @ Profile page for lecture rooms
    @ lecture room info
    +-- /user/$lecture_room?edit=true
        @ profile edit page



+-- /courses/
    @ course management page
    @ view all courses, with add course option
    +-- /courses/add
        @ course adding
        (editing is done in /course/$coursename?edit=true)

+-- /course/$coursename
    @ course profile
    +-- /course/$coursename?edit=true
        @ course edit page



+-- /trainers/
    @ trainers management page for training centers
    @ view all trainers, with add trainer option
    +-- /trainer/add
        @ trainer adding page
        (editing is done in /user/$trainer?edit=true)



+-- /search?query=query
    @ search page for trainers, training centers, courses and lecture rooms