/*
 *   Copyright (C) 2021 Johnny Mariéthoz.
 *
 * Coons is free software; you can redistribute it and/or modify it under the
 * terms of the MIT License; see LICENSE file for more details.
 */

import React from "react";
import { Card, List } from "semantic-ui-react";

export const CoonsResultsGridItem = ({ result, index }) => {
    const contributors = result.metadata.contributors || [];
    return (
      <Card fluid key={index} href={`/records/${result.id}`}>
        <Card.Content>
          <Card.Header>{result.metadata.title}</Card.Header>
          <Card.Description>
            {contributors && (
              <List horizontal relaxed>
                {contributors.map((contributor, idx) => (
                  <List.Item key={idx}>{contributor.name}</List.Item>
                ))}
              </List>
            )}
          </Card.Description>
        </Card.Content>
      </Card>
    );
  };

export default CoonsResultsGridItem;


