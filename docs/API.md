# API Documentation

This document provides detailed API documentation for the ILSpy MCP Server.

## Overview

The ILSpy MCP Server provides a Model Context Protocol (MCP) interface to the ILSpy .NET decompiler. It exposes four main tools and two prompts for interacting with .NET assemblies.

## Tools

### 1. decompile_assembly

Decompiles a .NET assembly to C# source code.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `assembly_path` | string | ✓ | - | Path to the .NET assembly file (.dll or .exe) |
| `output_dir` | string | ✗ | null | Output directory for decompiled files |
| `type_name` | string | ✗ | null | Fully qualified name of specific type to decompile |
| `language_version` | string | ✗ | "Latest" | C# language version to use |
| `create_project` | boolean | ✗ | false | Create a compilable project with multiple files |
| `show_il_code` | boolean | ✗ | false | Show IL code instead of C# |
| `remove_dead_code` | boolean | ✗ | false | Remove dead code during decompilation |
| `nested_directories` | boolean | ✗ | false | Use nested directories for namespaces |

**Language Versions:**
- `CSharp1` through `CSharp12_0`
- `Preview` (latest preview features)
- `Latest` (default, most recent stable)

**Example:**
```json
{
  "name": "decompile_assembly",
  "arguments": {
    "assembly_path": "/path/to/MyAssembly.dll",
    "type_name": "MyNamespace.MyClass",
    "language_version": "CSharp10_0",
    "remove_dead_code": true
  }
}
```

**Response:**
Returns decompiled C# source code as text, or information about saved files if `output_dir` is specified.

### 2. list_types

Lists types (classes, interfaces, structs, etc.) in a .NET assembly.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `assembly_path` | string | ✓ | - | Path to the .NET assembly file (.dll or .exe) |
| `entity_types` | array[string] | ✗ | ["c"] | Types of entities to list |

**Entity Types:**
- `c` - Classes
- `i` - Interfaces
- `s` - Structs
- `d` - Delegates
- `e` - Enums

**Example:**
```json
{
  "name": "list_types",
  "arguments": {
    "assembly_path": "/path/to/MyAssembly.dll",
    "entity_types": ["c", "i", "s"]
  }
}
```

**Response:**
Returns a formatted list of types organized by namespace, including:
- Type name
- Full qualified name
- Type kind (Class, Interface, etc.)
- Namespace

### 3. generate_diagrammer

Generates an interactive HTML diagrammer for visualizing assembly structure.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `assembly_path` | string | ✓ | - | Path to the .NET assembly file (.dll or .exe) |
| `output_dir` | string | ✗ | null | Output directory for the diagrammer |
| `include_pattern` | string | ✗ | null | Regex pattern for types to include |
| `exclude_pattern` | string | ✗ | null | Regex pattern for types to exclude |

**Example:**
```json
{
  "name": "generate_diagrammer",
  "arguments": {
    "assembly_path": "/path/to/MyAssembly.dll",
    "output_dir": "./diagrams",
    "include_pattern": "MyNamespace\\..+"
  }
}
```

**Response:**
Returns success status and output directory path. The HTML file can be opened in a web browser to view the interactive diagram.

### 4. get_assembly_info

Gets basic information about a .NET assembly.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `assembly_path` | string | ✓ | - | Path to the .NET assembly file (.dll or .exe) |

**Example:**
```json
{
  "name": "get_assembly_info",
  "arguments": {
    "assembly_path": "/path/to/MyAssembly.dll"
  }
}
```

**Response:**
Returns assembly metadata including:
- Assembly name
- Version
- Full name
- Location
- Target framework (if available)
- Runtime version (if available)
- Whether the assembly is signed
- Whether debug information is available

## Prompts

### 1. analyze_assembly

Provides a structured prompt for analyzing a .NET assembly and understanding its structure.

**Arguments:**

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `assembly_path` | string | ✓ | Path to the .NET assembly file |
| `focus_area` | string | ✗ | Specific area to focus on (types, namespaces, dependencies) |

**Example:**
```json
{
  "name": "analyze_assembly",
  "arguments": {
    "assembly_path": "/path/to/MyAssembly.dll",
    "focus_area": "types"
  }
}
```

### 2. decompile_and_explain

Provides a structured prompt for decompiling a specific type and explaining its functionality.

**Arguments:**

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `assembly_path` | string | ✓ | Path to the .NET assembly file |
| `type_name` | string | ✓ | Fully qualified name of the type to analyze |

**Example:**
```json
{
  "name": "decompile_and_explain",
  "arguments": {
    "assembly_path": "/path/to/MyAssembly.dll",
    "type_name": "MyNamespace.ImportantClass"
  }
}
```

## Error Handling

The server provides detailed error messages for common issues:

### Validation Errors
- Empty or invalid assembly paths
- Non-existent files
- Invalid file extensions (must be .dll or .exe)
- Invalid reference paths

### Runtime Errors
- ILSpyCmd not found or not installed
- Permission issues accessing files
- Decompilation failures
- Invalid assembly format

### Error Response Format
```json
{
  "content": [
    {
      "type": "text",
      "text": "Validation Error: Assembly file not found: /invalid/path.dll"
    }
  ]
}
```

## Data Models

### DecompileRequest
```python
class DecompileRequest(BaseModel):
    assembly_path: str
    output_dir: Optional[str] = None
    type_name: Optional[str] = None
    language_version: LanguageVersion = LanguageVersion.LATEST
    create_project: bool = False
    show_il_code: bool = False
    remove_dead_code: bool = False
    nested_directories: bool = False
    # ... additional fields
```

### TypeInfo
```python
class TypeInfo(BaseModel):
    name: str
    full_name: str
    kind: str
    namespace: Optional[str] = None
```

### AssemblyInfo
```python
class AssemblyInfo(BaseModel):
    name: str
    version: str
    full_name: str
    location: str
    target_framework: Optional[str] = None
    runtime_version: Optional[str] = None
    is_signed: bool = False
    has_debug_info: bool = False
```

## Usage Examples

### Basic Decompilation
```python
# Using the MCP client
result = await session.call_tool(
    "decompile_assembly",
    {"assembly_path": "MyApp.dll"}
)
```

### Filtered Type Listing
```python
# List only classes and interfaces
result = await session.call_tool(
    "list_types",
    {
        "assembly_path": "MyApp.dll",
        "entity_types": ["c", "i"]
    }
)
```

### Targeted Decompilation
```python
# Decompile specific type with optimizations
result = await session.call_tool(
    "decompile_assembly",
    {
        "assembly_path": "MyApp.dll",
        "type_name": "MyApp.Core.Engine",
        "language_version": "CSharp11_0",
        "remove_dead_code": true
    }
)
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOGLEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |

### MCP Client Configuration

For Claude Desktop:
```json
{
  "mcpServers": {
    "ilspy": {
      "command": "ilspy-mcp-server"
    }
  }
}
```

For development:
```json
{
  "mcpServers": {
    "ilspy": {
      "command": "python",
      "args": ["-m", "ilspy_mcp_server.server"],
      "env": {
        "LOGLEVEL": "DEBUG"
      }
    }
  }
}
```