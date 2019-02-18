from core import db


def check_existing_entries(model_column, column_values):
    """ Get a list of values from a model, where entries with those values
    already exist in the database.

        Args:
            model_column (object): column to check in the form `Model.Column`
            column_values (list): list of values to check - these
                should ideally be unique for the model.

        Returns:
            list: Values of entries that are already in the database

    """
    return [
        value[0] for value in db.session.query(
            model_column
        ).filter(
            model_column.in_(column_values)
        ).all()
    ]
