#include <nanobind/nanobind.h>
#include "WaferSimulator.h"

namespace nb = nanobind;

NB_MODULE(wafer_simulator, m) {
    m.doc() = "WaferSimulator module exposed to Python using nanobind";

    nb::class_<WaferSimulator>(m, "WaferSimulator")
    .def(nb::init<double, double, double, double, double>(),
         "Constructor with deltaT, X/Y limits, mass, dragCoeff",
         nb::arg("deltaT"), nb::arg("limitX"), nb::arg("limitY"), nb::arg("mass") = 1.0, nb::arg("dragCoeff") = 0.0)
        .def("update", &WaferSimulator::update, "Update the wafer position based on current forces")
        .def("setForce", [](WaferSimulator &sim, double fx, double fy) {
                sim.setForce({fx, fy});
            }, "Set a 2D force",
            nb::arg("fx"), nb::arg("fy"))
        .def("reset", &WaferSimulator::reset, "Reset the wafer to initial position and velocity")
        .def("getPosition", [](const WaferSimulator &sim) {
            auto p = sim.getPosition();
            return nb::make_tuple(p.x(), p.y());   // <-- use make_tuple
        })
        .def("getVelocity", [](const WaferSimulator &sim) {
            auto v = sim.getVelocity();
            return nb::make_tuple(v.x(), v.y());
        })
        .def("getForce", [](const WaferSimulator &sim) {
            auto f = sim.getForce();
            return nb::make_tuple(f.x(), f.y());
        })
        .def("getLimits", [](const WaferSimulator &sim) {
            auto l = sim.getLimits();
            return nb::make_tuple(l.x(), l.y());
        });
}
