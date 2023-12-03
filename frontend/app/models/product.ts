// id: int = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
//     product: str = db.Column(db.String(255), index=True)
//     brand: str = db.Column(db.String(255), index=True)
//     price: float = db.Column(db.Float)
//     rating: int = db.Column(db.Integer)
//     review: str = db.Column(db.Text)
//     votes: int = db.Column(db.Integer)

export interface Product {
    id: number;
    product: string;
    brand: string;
    price: number;
    rating: number;
    review: string;
    votes: number;
}