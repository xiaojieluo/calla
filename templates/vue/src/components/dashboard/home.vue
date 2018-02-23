<template lang="html">
  <div class="container">
      {{ msg }}
      <br>
      <Button @click="publish">Publish</Button>
  </div>
</template>

<script>
export default {
    data() {
        return {
            msg: 'Hello, dashboard.home'
        }
    },
    methods: {
        // 发布博文
        publish: function(){
            
        }
    }
}
</script>

<style lang="css">
</style>
