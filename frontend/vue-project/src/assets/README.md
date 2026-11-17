# Assets

This folder contains SVG illustrations for the Snack Overflow app.

## Current Assets

- `snack-packet.svg` - Orange snack packet illustration
- `cookie.svg` - Golden cookie with chocolate chips
- `mug.svg` - Coffee/tea mug illustration
- `chili-flake.svg` - Decorative chili flake shape

## Adding Custom Images

You can drop your own transparent WebP or PNG cutouts in this folder. Recommended:
- Transparent background (PNG/WebP with alpha)
- Consistent color palette (warm food colors)
- 64x64px or 128x128px for icons
- 512x512px or larger for hero illustrations

## Using Assets

Import SVGs in Vue components:

```vue
<script setup lang="ts">
import snackPacket from '@/assets/snack-packet.svg';
</script>

<template>
  <img :src="snackPacket" alt="Snack packet" />
</template>
```
