cmake_minimum_required(VERSION 3.18)

project(WaferAlignment LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# --- Python ---
find_package(Python 3.8 COMPONENTS Interpreter Development.Module REQUIRED)

# --- Fetch nanobind ---
include(FetchContent)
FetchContent_Declare(
  nanobind
  GIT_REPOSITORY https://github.com/wjakob/nanobind.git
  GIT_TAG v0.6.0
)
FetchContent_MakeAvailable(nanobind)

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

# --- Fetch GTest ---
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/release-1.14.0.zip
)
# For Windows: prevent overriding default compiler flags
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# --- Tests ---
enable_testing()
file(GLOB TEST_SRC "simulator_tests/*.cpp")
add_executable(simulator_tests ${TEST_SRC})
target_link_libraries(simulator_tests PRIVATE simulator_lib GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(simulator_tests)
