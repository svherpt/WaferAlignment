#include <nanobind/nanobind.h>
#include "WaferSimulator.h"

namespace nb = nanobind;

NB_MODULE(wafer_simulator, m) {
    m.doc() = "WaferSimulator module exposed to Python using nanobind";

    nb::enum_<ForceMode2D>(m, "ForceMode2D")
        .value("Local", ForceMode2D::Local)
        .value("World", ForceMode2D::World)
        .export_values();

    nb::class_<WaferSimulator>(m, "WaferSimulator")
        .def(nb::init<double, double, double, double, double, double, double>(),
             "Constructor with deltaT, X/Y limits, size, mass, dragCoeff, rotDragCoeff",
             nb::arg("deltaT"),
             nb::arg("limitX"),
             nb::arg("limitY"),
             nb::arg("size"),
             nb::arg("mass") = 1.0,
             nb::arg("dragCoeff") = 0.0,
             nb::arg("rotDragCoeff") = 0.0)
        .def("update", &WaferSimulator::update, "Update the wafer state")
        .def("reset", &WaferSimulator::reset, "Reset the wafer to initial state")
        .def("applyForce", [](WaferSimulator &sim, double fx, double fy) {
            sim.applyForce({fx, fy});
        }, "Apply force at the centre of mass", nb::arg("fx"), nb::arg("fy"))
        .def("applyForceAtPoint", [](WaferSimulator &sim, double fx, double fy, double px, double py, ForceMode2D mode = ForceMode2D::Local) {
            sim.applyForceAtPoint({fx, fy}, {px, py}, mode);
        }, "Apply force at a point with mode (Local or World)",
           nb::arg("fx"), nb::arg("fy"), nb::arg("px"), nb::arg("py"), nb::arg("mode") = ForceMode2D::Local)
        .def("applyTorque", &WaferSimulator::applyTorque, "Apply torque directly", nb::arg("torque"))
        .def("getPosition", [](const WaferSimulator &sim) {
            auto p = sim.getPosition();
            return nb::make_tuple(p.x(), p.y());
        })
        .def("getVelocity", [](const WaferSimulator &sim) {
            auto v = sim.getVelocity();
            return nb::make_tuple(v.x(), v.y());
        })
        .def("getOrientation", &WaferSimulator::getOrientation)
        .def("getAngularVelocity", &WaferSimulator::getAngularVelocity)
        .def("getLimits", [](const WaferSimulator &sim) {
            auto l = sim.getLimits();
            return nb::make_tuple(l.x(), l.y());
        });
}
