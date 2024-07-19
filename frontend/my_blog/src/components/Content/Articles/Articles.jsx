import React from "react";
import styles from "./Articles.module.css";
import Article from "./Article/Article";

const Articles = ({ articles, onDelete, onUpdate }) => {
  return (
    <>
      {articles.map((article) => (
        <Article
          key={article.id}
          article={article}
          onDelete={onDelete}
          onUpdate={onUpdate}
        />
      ))}
    </>
  );
};

export default Articles;
