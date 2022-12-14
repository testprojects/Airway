import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtLocation 5.12

MapQuickItem {
    property string magneticTrackAngle: ""
    property color colorLabel: "#000"
    property double rotation: 0
    property double angleRoute: 0
    property string direction: ""
    zoomLevel: 6.7

    onAngleRouteChanged: {
        if (direction === "forward") {
            if (angleRoute > 0 && angleRoute <= 90) {
                anchorPoint.x = labelMagneticTrackAngle.width
                anchorPoint.y = labelMagneticTrackAngle.height
            } else if (angleRoute > 90 && angleRoute <= 180) {
                anchorPoint.x = labelMagneticTrackAngle.x
                anchorPoint.y = labelMagneticTrackAngle.height
            } else if (angleRoute > 180 && angleRoute <= 270) {
                anchorPoint.x = labelMagneticTrackAngle.width + 1
                anchorPoint.y = labelMagneticTrackAngle.height + 1
            } else if (angleRoute > 270 && angleRoute <= 360) {
                anchorPoint.x = labelMagneticTrackAngle.width
                anchorPoint.y = labelMagneticTrackAngle.height
            }
        }
        else {
            if (angleRoute > 0 && angleRoute <= 90) {
//                anchorPoint.x = labelMagneticTrackAngle.width
//                anchorPoint.y = labelMagneticTrackAngle.height
            } else if (angleRoute > 90 && angleRoute <= 180) {
                anchorPoint.x = labelMagneticTrackAngle.width
                anchorPoint.y = labelMagneticTrackAngle.height
            } else if (angleRoute > 180 && angleRoute <= 270) {
//                anchorPoint.x = -(labelMagneticTrackAngle.width + 1)
//                anchorPoint.y = labelMagneticTrackAngle.height + 1
            } else if (angleRoute > 270 && angleRoute <= 360) {
                anchorPoint.x = labelMagneticTrackAngle.width
//                anchorPoint.y = labelMagneticTrackAngle.height
            }
        }
    }

    FontMetrics {
        id: fontMetrics
        font.family: "Arial"
    }

    sourceItem: Row {
        Text {
            id: labelMagneticTrackAngle
            Layout.fillWidth: true
            color: colorLabel
            text: (angleRoute > 0 && angleRoute <= 180) ? magneticTrackAngle + "\u2B9E" : "\u2B9C" + magneticTrackAngle
            font.pixelSize: 6
            horizontalAlignment: Text.AlignHCenter
        }
        transform: Rotation { origin.x: anchorPoint.x; origin.y: anchorPoint.y; angle: rotation  }
    }

    function setRotation(rot) {
        angleRoute = rot;
        if (rot >= 0 && rot < 90)
            rotation = (90 - rot) * -1;
        else if (rot >= 90 && rot < 180)
            rotation = (90 - (180 - rot));
        else if (rot >= 180 && rot < 270)
            rotation = (270 - rot) * -1;
        else if (rot >= 270 && rot <= 360)
            rotation = (90 - (360 - rot));
    }
}
