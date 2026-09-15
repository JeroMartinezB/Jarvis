from app import db

class Abstract_Prompt_Type(db.Model):
    __tablename__ = 'abstract_prompt_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Abstract Prompt Type: {self.name}'


class Prompt(db.Model):
    __tablename__ = 'prompt'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    prompt_type = db.Column(
        db.Integer,
        db.ForeignKey('abstract_prompt_type.id')
        )

    def __repr__(self):
        return f'Prompt: {self.description}'


class Response(db.Model):
    __tablename__ = 'response'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    prompt_id = db.Column(
        db.Integer,
        db.ForeignKey('prompt.id')
    )

    def __repr__(self):
        return f'Response: {self.description}'