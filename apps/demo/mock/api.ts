export default [
  {
    url: '/api/agency',
    method: 'get',
    response: () => {
      return {
        code: 200,
        data: {
          id: 1,
          name: 'John Doe',
        },
      };
    },
  },
];
