#include <nanobind/nanobind.h>
#include "WaferSimulator.h"

namespace nb = nanobind;

NB_MODULE(wafer_simulator, m) {
    m.doc() = "WaferSimulator module exposed to Python using nanobind";

    // Expose the WaferSimulator class
    nb::class_<WaferSimulator>(m, "WaferSimulator")
        .def(nb::init<double, double>(), "Constructor with deltaT and limit",
             nb::arg("deltaT"), nb::arg("limit"))
        .def("update", &WaferSimulator::update, "Update the wafer position based on current speed")
        .def("setSpeed", &WaferSimulator::setSpeed, "Set a new speed", nb::arg("newSpeed"))
        .def("reset", &WaferSimulator::reset, "Reset the wafer to initial position and speed")
        .def("getPosition", &WaferSimulator::getPosition, "Get the current wafer position")
        .def("getSpeed", &WaferSimulator::getSpeed, "Get the current wafer speed")
        .def("getLimit", &WaferSimulator::getLimit, "Get the maximum allowed position");
}
