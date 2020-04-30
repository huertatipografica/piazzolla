new Vue({
    el: '#app',
    data() {
        return {
            settings: [8, 14, 20, 30].map(s => {
                return {
                    size: s,
                    opsz: s,
                    wght: 400
                }
            })
        }
    }
})