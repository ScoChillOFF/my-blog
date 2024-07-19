import React, { useEffect, useState } from "react";
import axios from "axios";
import styles from "./Articles.module.css";
import CreateArticleForm from "./CreateArticleForm/CreateArticleForm";
import Article from "./Article/Article";

const Articles = () => {
  const [articles, setArticles] = useState([]);

  async function getArticlesFromServer() {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/articles');
    setArticles(response.data);
  }

  function onCreate(targetArticle) {
    const newArticles = [targetArticle, ...articles];
    setArticles(newArticles);
  }

  function onDelete(targetArticle) {
    const newArticles = articles.filter((article) => article.id != targetArticle.id);
    setArticles(newArticles);
  }

  useEffect(() => {getArticlesFromServer()}, []);

  return (
    <>
      <CreateArticleForm onCreate={onCreate} />
      <div className={styles.divider}></div>
      {articles.map(
        (article) => <Article key={article.id} article={article} onDelete={onDelete} />
      )}
    </>
  );
};

export default Articles;
