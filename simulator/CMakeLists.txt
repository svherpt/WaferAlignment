cmake_minimum_required(VERSION 3.18)

project(WaferAlignment)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Python
find_package(Python 3.8 COMPONENTS Interpreter Development.Module REQUIRED)

# Nanobind
execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NANOBIND_DIR
)
set(nanobind_DIR ${NANOBIND_DIR})
find_package(nanobind CONFIG REQUIRED)

# --- Core simulator library ---
file(GLOB SIMULATOR_SRC "simulator/*.cpp")
add_library(simulator_lib ${SIMULATOR_SRC})
target_include_directories(simulator_lib PUBLIC simulator)

# --- Python bindings ---
nanobind_add_module(wafer_simulator
    bindings/wafer_simulator_bindings.cpp
)
target_link_libraries(wafer_simulator PRIVATE simulator_lib)

# Copy to python package
add_custom_command(TARGET wafer_simulator POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
            $<TARGET_FILE:wafer_simulator>
            ${CMAKE_CURRENT_SOURCE_DIR}/../python/
)

# Ensure __init__.py exists
set(INIT_PY "${CMAKE_CURRENT_SOURCE_DIR}/../python/__init__.py")
if(NOT EXISTS ${INIT_PY})
    file(WRITE ${INIT_PY} "")
endif()

# --- Tests ---
find_package(GTest CONFIG REQUIRED)
enable_testing()
file(GLOB TEST_SRC "simulator_tests/*.cpp")
add_executable(simulator_tests ${TEST_SRC})
target_link_libraries(simulator_tests PRIVATE simulator_lib GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(simulator_tests)
