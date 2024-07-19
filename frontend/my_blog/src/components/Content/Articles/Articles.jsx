import React, { useEffect, useState } from "react";
import axios from "axios";
import styles from "./Articles.module.css";
import Article from "./Article/Article";

const Articles = () => {
  const [articles, setArticles] = useState([]);

  async function getArticlesFromServer() {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/articles');
    setArticles(response.data);
  }

  function onDelete(targetArticle) {
    const newArticles = articles.filter((article) => article.id != targetArticle.id);
    setArticles(newArticles);
  }

  useEffect(() => {getArticlesFromServer()}, []);

  return (
    <>
      {articles.map(
        (article) => <Article key={article.id} article={article} onDelete={onDelete} />
      )}
    </>
  );
};

export default Articles;
