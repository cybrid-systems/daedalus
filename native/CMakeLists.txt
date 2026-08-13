# native/CMakeLists.txt — shared dense-solve kernel (issue #29)
#
#   cmake -S native -B native/build
#   cmake --build native/build
#
# Emits native/libdaed_solve.so (Linux) or native/libdaed_solve.dylib (macOS).
cmake_minimum_required(VERSION 3.16)
project(daedalus_native LANGUAGES CXX)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

add_library(daed_solve SHARED daed_solve.cpp)
target_include_directories(daed_solve PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}")
target_compile_features(daed_solve PRIVATE cxx_std_17)
set_target_properties(daed_solve PROPERTIES
  POSITION_INDEPENDENT_CODE ON
  OUTPUT_NAME daed_solve
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
)

if(APPLE)
  set_target_properties(daed_solve PROPERTIES SUFFIX ".dylib")
endif()
