set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/modules ${CMAKE_MODULE_PATH} )

find_package(LibRaw ${LIBRAW_MIN_VERSION} REQUIRED)
if(NOT ${LIBRAW_FOUND})
    message(FATAL_ERROR "** Unable to locate LibRaw.")
endif()

add_executable(generate_camera_info generate_camera_info.cpp)
target_compile_definitions(generate_camera_info PRIVATE ${LibRaw_DEFINITIONS})
target_include_directories(generate_camera_info PRIVATE ${LibRaw_INCLUDE_DIR} ${PROJECT_SOURCE_DIR}/third_party) 
target_link_libraries(generate_camera_info PRIVATE ${LibRaw_LIBRARIES})

set(CMAKE_CXX_STANDARD 17)