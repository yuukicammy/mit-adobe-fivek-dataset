set(CMAKE_MIN_VERSION   "3.5.0")
set(LIBRAW_MIN_VERSION  "0.21")

cmake_minimum_required(VERSION ${CMAKE_MIN_VERSION})

if(NOT DEFINED CMAKE_DEBUG_POSTFIX) 
    set(CMAKE_DEBUG_POSTFIX "d")
endif()

set(CMAKE_CXX_STANDARD 17)

project(fivek)

message(STATUS "----------------------------------------------------------------------------------")
message(STATUS "Starting CMake configuration for: ${PROJECT_NAME}")

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules ${CMAKE_MODULE_PATH} )

find_package(LibRaw ${LIBRAW_MIN_VERSION} REQUIRED)
if(NOT ${LIBRAW_FOUND})
    message(FATAL_ERROR "** Unable to locate LibRaw.")
endif()

add_executable(opendng open_dng.cpp)
target_compile_definitions(opendng PRIVATE ${LibRaw_DEFINITIONS})
target_include_directories(opendng PRIVATE ${LibRaw_INCLUDE_DIR}) 
target_link_libraries(opendng PRIVATE ${LibRaw_LIBRARIES})  
