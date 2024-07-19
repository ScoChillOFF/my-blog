import React, { useState, useEffect } from "react";
import axios from "axios";
import Articles from "./Articles/Articles.jsx";
import CreateArticleForm from "./CreateArticleForm/CreateArticleForm.jsx";
import FilterSection from "./FilterSection/FilterSection.jsx";
import styles from "./Content.module.css";

const Content = () => {
  const [articles, setArticles] = useState([]);

  async function getArticlesFromServer() {
    const response = await axios.get("http://127.0.0.1:8000/api/v1/articles");
    setArticles(response.data);
  }

  useEffect(() => {
    getArticlesFromServer();
  }, []);

  function onCreate(targetArticle) {
    const newArticles = [targetArticle, ...articles];
    setArticles(newArticles);
  }

  function onDelete(targetArticle) {
    const newArticles = articles.filter(
      (article) => article.id != targetArticle.id
    );
    setArticles(newArticles);
  }

  function onUpdate(targetArticle) {
    const newArticles = articles.map((article) =>
      article.id == targetArticle.id ? targetArticle : article
    );
    setArticles(newArticles);
  }

  function onApply(newArticles) {
    setArticles(newArticles);
  }

  return (
    <div className={styles.content}>
      <div className={styles.leftWrapper}>
        <CreateArticleForm onCreate={onCreate} />
        <div className={styles.divider}></div>
        <Articles articles={articles} onDelete={onDelete} onUpdate={onUpdate} />
      </div>
      <FilterSection onApply={onApply} />
    </div>
  );
};

export default Content;
