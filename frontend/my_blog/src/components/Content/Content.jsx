import React, { useState, useEffect } from "react";
import axios from "axios";
import Articles from "./Articles/Articles.jsx";
import CreateArticleForm from "./CreateArticleForm/CreateArticleForm.jsx";
import FilterSection from "./FilterSection/FilterSection.jsx";
import styles from "./Content.module.css";

const Content = () => {
  const [articles, setArticles] = useState([]);
  const [tags, setTags] = useState([]);
  const [appliedTagNames, setAppliedTagNames] = useState([]);

  useEffect(() => {
    getArticlesFromServer();
    getTagsFromServer();
  }, []);

  async function getArticlesFromServer() {
    const response = await axios.get("http://127.0.0.1:8000/api/v1/articles");
    setArticles(response.data);
  }

  async function getTagsFromServer() {
    const response = await axios.get("http://127.0.0.1:8000/api/v1/tags");
    setTags(response.data);
  }

  async function onCreate(targetArticle) {
    await getTagsFromServer();
    if (appliedTagNames.length == 0 || isAnyTagApplied(targetArticle)) {
      const newArticles = [targetArticle, ...articles];
      setArticles(newArticles);
    }
  }

  function isAnyTagApplied(article) {
    for (let tag of article.tags) {
      if (appliedTagNames.includes(tag.name)) {
        return true;
      }
    }
    return false;
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

  function onApply(newArticles, selectedTagNames) {
    setArticles(newArticles);
    setAppliedTagNames(selectedTagNames);
  }

  return (
    <div className={styles.content}>
      <div className={styles.leftWrapper}>
        <CreateArticleForm onCreate={onCreate} />
        <div className={styles.divider}></div>
        <Articles articles={articles} onDelete={onDelete} onUpdate={onUpdate} />
      </div>
      <FilterSection onApply={onApply} tags={tags} />
    </div>
  );
};

export default Content;
