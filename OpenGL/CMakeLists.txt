cmake_minimum_required(VERSION 3.21)
project(project)

set(CMAKE_CXX_STANDARD 14)

add_executable(project main.cpp)

find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)
find_package(GLEW REQUIRED)

message("OpenGL found")
message("include dir: ${OPENGL_INCLUDE_DIR}")
message("link libraries: ${OPENGL_LIBRARIES}")

message("GLUT found")
message("include dir: ${GLUT_INCLUDE_DIR}")
message("link libraries: ${GLUT_LIBRARIES}")

message("GLEW found")
message("include dir: ${GLEW_INCLUDE_DIR}")
message("link libraries: ${GLEW_LIBRARIES}")

target_link_libraries(
        ${PROJECT_NAME}
        PUBLIC
        OpenGL::GL
        GLUT::GLUT
        GLEW::GLEW
)
