#ifndef SETTINGSDIALOG_H
#define SETTINGSDIALOG_H

#include <QDialog>

namespace Ui {
    class SettingsDialog;
}

class SettingsDialog : public QDialog
{
        Q_OBJECT

    public:
        explicit SettingsDialog(QWidget *parent = nullptr);
        ~SettingsDialog();

    private:
        Ui::SettingsDialog *ui;
        void readSettings();

    private slots:
        void selectFileDatabase();
        void writeSettings();
        void addNewSourceDataToList();
        void removeSourceDataFromList();
        void enableRemoveButton();
};

#endif // SETTINGSDIALOG_H
