import pymongo
from bson import ObjectId


def search_author(authors=None, year_min=None, year_max=None):
    query = {}
    if authors is not None and len(authors) != 0:
        query.update({"name": {"$in": authors}})
    if year_min != '':
        year_min = int(year_min)
        query.update({"year_born": {"$gte": year_min}})
    if year_max != '':
        year_max = int(year_max)
        query.update({"year_dead": {"$lte": year_max}})

    query = query if len(query) != 0 else {"_id": {"$exists": "true"}}
    return {"$match": query}


def search_poem(poem_name=None):
    query = {}
    if poem_name is not None and poem_name != '':
        query.update({"poem_name": poem_name})
    query = query if len(query) != 0 else {"poem_name": {"$exists": "true"}}
    return {"$match": query}


def search_lemma(lemmas=None):
    query = {}
    if lemmas is not None and lemmas != '':
        lemmas = list(map(str.strip, lemmas.split(',')))
        query.update({"lemma": {"$in": lemmas}})
    query = query if len(query) != 0 else {"_id": {"$exists": "true"}}
    return {"$match": query}


def search_book(book_name=None, year_min=None, year_max=None, publishing_company=None):
    query = {}
    if book_name is not None and book_name != '':
        query.update({"book_name": book_name})
    year = {}
    if year_min is not None and year_min != '':
        year_min = int(year_min)
        year.update({"$gte": year_min})
    if year_max is not None and year_max != '':
        year_max = int(year_max)
        year.update({"$lte": year_max})
    if len(year) != 0:
        query.update({"year_published": year})
    if publishing_company is not None and len(publishing_company) != 0:
        query.update({"publishing_company": {"$in": publishing_company}})
    query = query if len(query) != 0 else {"book_name": {"$exists": "true"}}
    return {"$match": query}


def search_reference(persons=None):
    query = {}
    if persons is not None and len(persons) != 0:
        query.update({"person": {"$in": persons}})
    query = query if len(query) != 0 else {"_id": {"$exists": "true"}}
    return {"$match": query}


def sorting(year='year_born', direction=1):
    query = {"num_refs": -1, "name": 1, "poems.poem_name": 1}
    query.update({year: direction})
    return query


def main_search(db, authors=None, year_min_a=None, year_max_a=None,
                poem_name=None, persons_ref=None, book_name=None,
                year_min_pub=None, year_max_pub=None, publishing_company=None,
                lemmas=None, sort_year='year_born', sort_direction=1, skip=0):
    res = db.authors.aggregate([
            search_author(authors=authors, year_min=year_min_a, year_max=year_max_a),
            {
                "$lookup": {
                    "from": "poems",
                    "localField": "_id",
                    "foreignField": "author",
                    "pipeline": [search_poem(poem_name=poem_name)],
                    "as": "poems"
                }
            },
            {
                "$unwind": "$poems"
            },
            {
                "$lookup": {
                    "from": "references",
                    "localField": "poems._id",
                    "foreignField": "poem",
                    "pipeline": [search_reference(persons=persons_ref)],
                    "as": "references"
                }
            },
            {
                "$addFields": {
                    "book_id": "$poems.book",
                    "poem_id": "$poems._id",
                    "num_refs": {"$size":"$references"}
                }
            },
            {
                "$match": {"num_refs": {"$gt": 0}}
            },
            {
                "$lookup": {
                    "from": "books",
                    "localField": "book_id",
                    "foreignField": "_id",
                    "pipeline": [
                        search_book(
                            book_name=book_name,
                            year_min=year_min_pub,
                            year_max=year_max_pub,
                            publishing_company=publishing_company)
                    ],
                    "as": "books"
                }
            },
            {
                "$unwind": "$books"
            },
            (
                {
                    "$lookup": {
                        "from": "lemmas",
                        "let": {"poem_id": "$poem_id"},
                        "pipeline": [
                            {"$match": {"$expr": {"$in": ["$$poem_id", "$docs"]}}},
                            search_lemma(lemmas=lemmas),
                        ],
                        "as": "lemmas"
                    }
                }
                if lemmas is not None else {"$match": {"_id": {"$exists": "true"}}}
            ),
            (
                {
                "$match": {"$expr": {"$gt": [{"$size": "$lemmas"}, 0]}}
                }
                if lemmas is not None else {"$match": {"_id": {"$exists": "true"}}}
            ),
            {
                "$sort": sorting(year=sort_year, direction=sort_direction)
            },
            {
                "$limit": 5
            },
            {
                "$skip": skip
            },
            {
                "$project": {
                    "author": {
                        "name": "$name",
                        "year_born": "$year_born",
                        "year_dead": "$year_dead",
                    },
                    "author_born"
                    "num_refs": "$num_refs",
                    "poem": {
                        "poem_name": "$poems.poem_name",
                        "poem_name_2": "$poems.poem_name_2",
                        "text": "$poems.text"
                    },
                    "book": "$books",
                    "comment": "$poems.comment",
                    "references": "$references"
                }
            },
        ])
    return res



def fulltext_search(db, text, sort_year, sort_direction):
    results = db.poems.aggregate([
                {'$match':{'$text':{'$search':text}}},
                {
                    "$lookup": {
                        "from": "authors",
                        "localField": "author",
                        "foreignField": "_id",
                        "as": "authors"
                    }},
                {
                    "$unwind":"$authors"
                },
                {
                    "$lookup": {
                        "from": "references",
                        "localField": "_id",
                        "foreignField": "poem",
                        "as": "references"
                    }
                },
                {
                    "$addFields": {
                        "book_id": "$book",
                        "poem_id": "$_id",
                        "num_refs": {"$size":"$references"}
                    }
                },
                {
                    "$lookup": {
                        "from": "books",
                        "localField": "book_id",
                        "foreignField": "_id",
                        "as": "books"
                    }
                },
                {
                    "$unwind": "$books"
                },
                {
                    "$sort": sorting(year=sort_year, direction=sort_direction)
                },
                {
                    "$limit": 5
                },
                {
                  "$skip": skip
                },
                {
                    "$project": {
                        "author": {
                            "name": "$authors.name",
                            "year_born": "$authors.year_born",
                            "year_dead": "$authors.year_dead",
                        },
                        "author_born"
                        "num_refs": "$num_refs",
                        "poem": {
                            "poem_name": "$poem_name",
                            "poem_name_2": "$poem_name_2",
                            "text": "$text"
                        },
                        "book": "$books",
                        "comment": "$comment",
                        "references": "$references"
                    }
                },
            ])
    return results
