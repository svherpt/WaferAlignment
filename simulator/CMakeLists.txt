cmake_minimum_required(VERSION 3.18)

project(WaferSimulatorPythonBindings)

# --- Use C++20 globally ---
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# --- Python detection ---
if (CMAKE_VERSION VERSION_LESS 3.18)
    set(DEV_MODULE Development)
else()
    set(DEV_MODULE Development.Module)
endif()

find_package(Python 3.8 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

# --- Default build type ---
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# --- Nanobind detection ---
execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NANOBIND_DIR
)
set(nanobind_DIR ${NANOBIND_DIR})
find_package(nanobind CONFIG REQUIRED)

# --- Core simulator library ---
# Paths are now relative to CMakeLists.txt (simulator/)
add_library(simulator_lib
    simulator/WaferSimulator.cpp
)

target_include_directories(simulator_lib PUBLIC
    simulator
)

# --- Python module ---
nanobind_add_module(wafer_simulator
    bindings/wafer_simulator_bindings.cpp
)

# Link core simulator library to Python module
target_link_libraries(wafer_simulator PRIVATE simulator_lib)

# Force output name (optional, matches import)
set_target_properties(wafer_simulator PROPERTIES OUTPUT_NAME "wafer_simulator")

# --- Copy .pyd to python/ folder after build ---
add_custom_command(TARGET wafer_simulator POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
            $<TARGET_FILE:wafer_simulator>
            ${CMAKE_CURRENT_SOURCE_DIR}/../python/
)

# --- Make python/ a package (ensure __init__.py exists) ---
set(INIT_PY "${CMAKE_CURRENT_SOURCE_DIR}/../python/__init__.py")
if(NOT EXISTS ${INIT_PY})
    file(WRITE ${INIT_PY} "")
endif()
