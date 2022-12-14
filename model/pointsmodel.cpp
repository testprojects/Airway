#include "pointsmodel.h"
#include <QDebug>

PointsModel::PointsModel(QObject *parent) : QAbstractTableModel(parent),
    m_checkedRows(QList<bool>())
{
    m_headers << tr("*")
              << tr("Code airway")
              << tr("Name PPM")
              << tr("Latitude")
              << tr("Longitude")
              << tr("MPU")
              << tr("Distance")
              << tr("Upper/lower limit")
              << tr("Minimum altitude")
              << tr("Width")
              << tr("Direction trains");
}

PointsModel::~PointsModel()
= default;

int PointsModel::rowCount(const QModelIndex &parent) const
{
    Q_UNUSED(parent)

    return m_points.size();
}

int PointsModel::columnCount(const QModelIndex &parent) const
{
    Q_UNUSED(parent)

    return m_headers.size();
}

QVariant PointsModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid())
        return QVariant();

    int row = index.row();
    int col = index.column();

    if (index.column() == 0 && role == Qt::CheckStateRole)
        return (!m_checkedRows.empty() && m_checkedRows.at(row)) ? Qt::Checked : Qt::Unchecked;

    if (role == Qt::DisplayRole)
        return m_points.at(row).toList().at(col - 1);

    return QVariant();
}

QVariant PointsModel::headerData(int section, Qt::Orientation orientation, int role) const
{
    if (section > m_headers.size() || orientation != Qt::Horizontal || role != Qt::DisplayRole)
        return QVariant();

    return m_headers.at(section);
}

Qt::ItemFlags PointsModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::ItemIsEnabled;

    return QAbstractTableModel::flags(index) | Qt::ItemIsEditable;
}

bool PointsModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (index.isValid() && index.column() == 0 && role == Qt::CheckStateRole) {
        m_checkedRows[index.row()] = value.toBool();
        emit dataChanged(index, index, {role});
        return true;
    }
    return false;
}

//void PointsModel::fetchMore(const QModelIndex &parent)
//{
//    int remainder = m_points.size() - m_pointCount;
//    int rowsToFetch = qMin(100, remainder);

//    if (rowsToFetch <= 0)
//        return;

//    beginInsertRows(QModelIndex(), m_pointCount, m_pointCount + rowsToFetch - 1);

//    m_pointCount += rowsToFetch;

//    endInsertRows();
//}

//bool PointsModel::canFetchMore(const QModelIndex &parent) const
//{
//    return (m_pointCount < m_points.size());
//}

void PointsModel::setDataModel(const QList<QVariant> &data)
{
    beginResetModel();
    m_points = data;

    for (int i = 0; i < m_points.size(); i++)
        m_checkedRows.append(false);
    endResetModel();
}

QStringList PointsModel::getMagneticTrackAngle(const QModelIndex &index) const
{
    if (!index.isValid())
        return {};

    if (m_points.at(index.row()).toList().at(4).toString().isEmpty() &&
            m_points.at(index.row()).toList().at(5).toString().isEmpty())
        return {};

    return QStringList() << m_points.at(index.row()).toList().at(4).toString()
                         << m_points.at(index.row()).toList().at(5).toString();
}

double PointsModel::getDistance(const QModelIndex &index) const
{
    if (!index.isValid())
        return {};

    return 0;
}

double PointsModel::getMinimumAltitude(const QModelIndex &index) const
{
    if (!index.isValid())
        return {};

    return m_points.at(index.row()).toList().at(6).toDouble();
}

double PointsModel::getWidth(const QModelIndex &index) const
{
    if (!index.isValid())
        return {};

    return m_points.at(index.row()).toList().at(7).toDouble();
}

QStringList PointsModel::getDirectionTrains(const QModelIndex &index) const
{
    if (!index.isValid())
        return {};

    if (m_points.at(index.row()).toList().at(8).toString().isEmpty() &&
            m_points.at(index.row()).toList().at(9).toString().isEmpty())
        return {};

    return QStringList() << m_points.at(index.row()).toList().at(8).toString()
                         << m_points.at(index.row()).toList().at(9).toString();
}

QStringList PointsModel::getLimit(const QModelIndex &index) const
{
    if (!index.isValid())
        return {};

    if (m_points.at(index.row()).toList().at(10).toString().isEmpty() &&
            m_points.at(index.row()).toList().at(11).toString().isEmpty())
        return {};

    return QStringList() << m_points.at(index.row()).toList().at(10).toString()
                         << m_points.at(index.row()).toList().at(11).toString();
}
