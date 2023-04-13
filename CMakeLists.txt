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

add_subdirectory(tools)