# GraphML Format Guide for graphml-to-falkordb

This guide explains the GraphML format expected by the graphml-to-falkordb tool.

## Required Structure

Your GraphML file must include proper key definitions for all attributes. Here's the minimal structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <!-- Define keys for node and edge attributes -->
  <key id="node_label" for="node" attr.name="label" attr.type="string"/>
  <key id="edge_label" for="edge" attr.name="label" attr.type="string"/>
  <key id="name" for="node" attr.name="name" attr.type="string"/>

  <graph id="G" edgedefault="directed">
    <!-- Nodes -->
    <node id="n1">
      <data key="node_label">Person</data>
      <data key="name">Alice</data>
    </node>

    <!-- Edges -->
    <edge id="e1" source="n1" target="n2">
      <data key="edge_label">KNOWS</data>
    </edge>
  </graph>
</graphml>
```

## Key Components

### 1. Key Definitions

Define all attributes that you'll use:

```xml
<key id="unique_id" for="node|edge" attr.name="attribute_name" attr.type="string|int|double|boolean"/>
```

- `id`: Unique identifier for the key (e.g., `node_label`, `name`)
- `for`: Where this attribute applies: `node` or `edge`
- `attr.name`: The actual attribute name stored in FalkorDB
- `attr.type`: Data type - `string`, `int`, `double`, `boolean`

### 2. Node Labels

Nodes must have a `label` attribute that will become their label in FalkorDB:

```xml
<node id="n1">
  <data key="node_label">Person</data>
  <data key="name">Alice</data>
  <data key="age">30</data>
</node>
```

This creates a node with:
- Label: `Person`
- Properties: `name: "Alice"`, `age: "30"`

### 3. Edge Labels (Relationship Types)

Edges must have a `label` attribute that becomes the relationship type in FalkorDB:

```xml
<edge id="e1" source="n1" target="n2">
  <data key="edge_label">KNOWS</data>
  <data key="since">2020</data>
</edge>
```

This creates a relationship:
- Type: `KNOWS`
- Properties: `since: "2020"`

## Complete Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">

  <!-- Define all keys -->
  <key id="node_label" for="node" attr.name="label" attr.type="string"/>
  <key id="name" for="node" attr.name="name" attr.type="string"/>
  <key id="age" for="node" attr.name="age" attr.type="int"/>
  <key id="founded" for="node" attr.name="founded" attr.type="int"/>
  <key id="edge_label" for="edge" attr.name="label" attr.type="string"/>
  <key id="since" for="edge" attr.name="since" attr.type="int"/>
  <key id="position" for="edge" attr.name="position" attr.type="string"/>

  <graph id="G" edgedefault="directed">
    <!-- Person nodes -->
    <node id="n1">
      <data key="node_label">Person</data>
      <data key="name">Alice</data>
      <data key="age">30</data>
    </node>
    <node id="n2">
      <data key="node_label">Person</data>
      <data key="name">Bob</data>
      <data key="age">35</data>
    </node>

    <!-- Company node -->
    <node id="n3">
      <data key="node_label">Company</data>
      <data key="name">TechCorp</data>
      <data key="founded">2010</data>
    </node>

    <!-- Relationships -->
    <edge id="e1" source="n1" target="n2">
      <data key="edge_label">KNOWS</data>
      <data key="since">2020</data>
    </edge>
    <edge id="e2" source="n1" target="n3">
      <data key="edge_label">WORKS_AT</data>
      <data key="position">Engineer</data>
    </edge>
    <edge id="e3" source="n2" target="n3">
      <data key="edge_label">WORKS_AT</data>
      <data key="position">Manager</data>
    </edge>
  </graph>
</graphml>
```

## Important Notes

1. **Node IDs** (`id` attribute on `<node>`) must be unique and will be stored as properties in FalkorDB for reference

2. **Node Labels** - Every node must have a `label` attribute defined via a data key. If missing, the default label is `Node`

3. **Edge Labels** - Every edge must have a `label` attribute defined via a data key. If missing, the default type is `RELATES_TO`

4. **Data Types** - Use the correct type in the key definition:
   - `string` - Text
   - `int` - Integers
   - `double` - Decimal numbers
   - `boolean` - true/false

5. **Graph Direction** - Use `edgedefault="directed"` for directed graphs or `edgedefault="undirected"` for undirected graphs

## Generating GraphML

Many tools can generate GraphML:
- **yEd** - Visual editor (exports to GraphML)
- **Gephi** - Network analysis tool
- **NetworkX** - Python library
- **Cytoscape** - Interactive visualization

## Troubleshooting

- **Error: "no key X"** - You referenced a key in `<data>` but didn't define it in `<key>`
- **Missing labels** - Ensure every node has a `label` data element
- **Missing relationship types** - Ensure every edge has a `label` data element
